(function () {
  'use strict';

  const lab = window.MG_SPACE_LAB_V23;
  const $ = id=>document.getElementById(id);
  if (!lab) {
    $('lab-intro').textContent = '試算模型載入失敗。請確認套件完整。 / Models unavailable. Check the package contents.';
    return;
  }
  const esc = value=>String(value??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const supported = 'zh-TW en zh-CN ja ko es fr de pt it nl ru uk pl cs sk sl hr sr bg ro hu el tr ar he fa ur hi bn ta te mr gu kn ml pa ne si th vi id ms fil km lo my mn kk uz az ka hy sw am ha yo ig zu af so sv no da fi is et lv lt ga cy mt sq mk bs eu gl ca eo'.split(' ');
  const query = new URLSearchParams(location.search);
  const course = /^[a-z0-9_-]{1,100}$/.test(query.get('course')||'') ? query.get('course') : '';
  const modelFor = id=>lab.models.find(model=>model.id===id);
  const recordKey = 'mg-space-lab-v23-records:'+(course||'general');
  const U = window.MG_CAMPAIGN_UTILS||{};
  let preference = query.get('lang');
  try { preference ||= localStorage.getItem('mg-language'); } catch { /* Offline or restricted storage. */ }
  const resolve = choice=>U.resolveSupportedLanguage?.(choice,navigator,supported) || (String(choice||navigator.language).startsWith('zh')?'zh-TW':'en');
  let language = resolve(preference||'auto');
  let current = modelFor(location.hash.slice(1)) || modelFor(query.get('model')) || lab.models[0];
  let values = lab.defaults(current.id), locale, cloud, hostedTranslation = false, frame = 0;
  let recordMessage = '';

  function readRecords() {
    try {
      const raw = JSON.parse(sessionStorage.getItem(recordKey)||'[]');
      if (!Array.isArray(raw)) return [];
      return raw.slice(-50).flatMap(row=>{
        if (!row || !modelFor(row.model) || typeof row.at!=='string' || !Number.isFinite(Date.parse(row.at))) return [];
        try {
          const result = lab.calculate(row.model,row.inputs);
          const inputs = Object.fromEntries(modelFor(row.model).inputs.map(field=>[field.key,row.inputs[field.key]]));
          return [{model:row.model,inputs,result,at:row.at}];
        }
        catch { return []; }
      });
    } catch { return []; }
  }
  let records = readRecords();
  const pick = pair=>pair[language==='zh-TW'?0:1];
  const t = (zh,en)=>pick([zh,en]);
  const text = (id,value)=>{$(id).textContent=value;};
  const unitValue = (value,unit)=>`${format(value)} ${unit}`;

  function format(value) {
    if (value===0) return '0';
    const abs = Math.abs(value);
    const options = {maximumSignificantDigits: 6, ...(abs>=1e8 || abs<.0001 ? {notation:'scientific'} : {})};
    return new Intl.NumberFormat(language,options).format(value);
  }

  function drawCurve(result) {
    const input = current.inputs.find(field=>field.key===current.sweep)||current.inputs[0], output = current.outputs[0];
    const value = values[input.key], radius = Math.max(Math.abs(value)*.35,Math.abs(input.value)*.2,input.step*6);
    const low = Math.max(input.min,value-radius), high = Math.min(input.max,value+radius);
    if (!(high>low)) { $('curve').hidden=true; return; }
    const sample = Array.from({length:41},(_,index)=>{
      const x = low+(high-low)*index/40;
      try { return lab.calculate(current.id,{...values,[input.key]:input.integer?Math.round(x):x})[output.key]; }
      catch { return null; }
    });
    const valid = sample.filter(value=>value!==null);
    if (valid.length<2) { $('curve').hidden=true; return; }
    valid.push(result[output.key]);
    const lo = Math.min(...valid), hi = Math.max(...valid);
    const sy = value=>lo===hi ? 43 : 75-62*(value-lo)/(hi-lo);
    let path = '', pen = false;
    sample.forEach((y,index)=>{
      if (y===null) { pen=false; return; }
      path += `${pen?'L':'M'}${(12+336*index/40).toFixed(2)} ${sy(y).toFixed(2)} `;
      pen = true;
    });
    const dotX = 12+336*(value-low)/(high-low), dotY = sy(result[output.key]);
    $('curve-plot').innerHTML = `<path d="M12 12V76H348M12 44H348" fill="none" stroke="#426079" stroke-width="1" stroke-dasharray="3 3"/><path d="${path}" stroke="#92e6d9" stroke-width="2.2" fill="none" vector-effect="non-scaling-stroke"/><circle cx="${dotX.toFixed(2)}" cy="${dotY.toFixed(2)}" r="4.8" fill="#ffd292" stroke="#0a1a2c" stroke-width="1.3"/>`;
    text('curve-low',unitValue(low,input.unit));
    text('curve-high',unitValue(high,input.unit));
    text('curve-note',t('固定其餘輸入，橫軸改變','Sweep')+' '+pick(input.label)+' · '+t('縱軸範圍','Output range')+' '+format(lo)+' … '+unitValue(hi,output.unit));
    $('curve').hidden=false;
  }

  function errorText(error) {
    const ranges = {
      'mass-order': ['終態質量必須小於或等於初始質量。','Final mass must be at most the initial mass.'],
      'no-thermal-sink': ['目前淨散熱通量為零或負值。請降低熱沉溫度或外部吸收，或提高散熱面溫度。','Net heat rejection is zero or negative. Lower the sink temperature or absorbed flux, or raise radiator surface temperature.'],
      'wheel-initial': ['初始輪動量已高於輪動量容量。','Initial wheel momentum exceeds capacity.'],
      'phasing-altitude': ['另一側拱點高度低於 150 km 的教學下界。請增加相位圈數或縮小相位角。','The opposite apsis falls below the 150 km teaching floor. Increase phasing laps or reduce the lead angle.']
    };
    if (error.message==='invalid-input') {
      const field = current.inputs.find(input=>input.key===error.field);
      if (field) return `${pick(field.label)} · ${t('請輸入','Enter')} ${format(field.min)} … ${unitValue(field.max,field.unit)}${field.integer?t(' 的整數',' (integer)'):''}`;
    }
    return pick(ranges[error.message]||['請檢查輸入值。','Check the input values.']);
  }

  function compute() {
    let result, invalid;
    try { result=lab.calculate(current.id,values); } catch (error) { invalid=error; }
    for (const field of current.inputs) $(`number-${field.key}`).setAttribute('aria-invalid',String(invalid?.field===field.key));
    $('input-error').hidden = !invalid;
    text('input-error',invalid ? errorText(invalid) : '');
    $('record').disabled = !!invalid;
    for (const field of current.outputs) text(`result-${field.key}`,result ? unitValue(result[field.key],field.unit) : '—');
    if (result) drawCurve(result); else $('curve').hidden=true;
    return result;
  }
  function queueCompute() {
    if (frame) return;
    frame=requestAnimationFrame(()=>{frame=0;compute();});
  }

  function renderControls() {
    $('controls').innerHTML = current.inputs.map(field=>{
      const {key,unit,min,max,step,integer} = field;
      return `<div class="input-row"><div class="input-head"><label for="number-${key}" id="label-${key}">${esc(pick(field.label))}<br><small data-no-translate>${esc(unit)}</small></label><input class="number-input" type="number" id="number-${key}" min="${min}" max="${max}" step="${integer?1:'any'}" inputmode="${integer?'numeric':'decimal'}" aria-describedby="limits-${key}"></div><input class="range-input" type="range" id="range-${key}" min="${min}" max="${max}" step="${step}" aria-labelledby="label-${key}"><div class="limits" id="limits-${key}" data-no-translate><span>${esc(unitValue(min,unit))}</span><span>${esc(unitValue(max,unit))}</span></div></div>`;
    }).join('');
    for (const field of current.inputs) {
      const {key,min,max} = field, number = $(`number-${key}`), range = $(`range-${key}`);
      number.value = Number.isFinite(values[key]) ? values[key] : '';
      range.value = Number.isFinite(values[key]) ? values[key] : field.value;
      number.addEventListener('input',()=>{
        values[key]=number.valueAsNumber;
        if (values[key]>=min && values[key]<=max) range.value=values[key];
        queueCompute();
      });
      range.addEventListener('input',()=>{values[key]=range.valueAsNumber;number.value=range.value;queueCompute();});
    }
    $('results').innerHTML = current.outputs.map((field,index)=>`<div class="result-row${index===0?' hero-result':''}"><dt>${esc(pick(field.label))}</dt><dd><output id="result-${field.key}" data-no-translate>—</output></dd></div>`).join('');
  }

  function renderRecords() {
    $('export').disabled=!records.length;
    text('record-status',recordMessage);
    if (!records.length) { text('record-list',t('尚無紀錄。','No experiments recorded yet.')); return; }
    const rows = [...records].reverse().map(record=>{
      const model = modelFor(record.model), first = model.outputs[0], date = new Intl.DateTimeFormat(language,{dateStyle:'short',timeStyle:'short'}).format(new Date(record.at));
      return `<tr><td>${esc(date)}</td><td>${esc(pick(model.title))}</td><td>${esc(unitValue(record.result[first.key],first.unit))}</td></tr>`;
    }).join('');
    $('record-list').innerHTML=`<table><thead><tr><th scope="col">${t('時間','Time')}</th><th scope="col">${t('模型','Model')}</th><th scope="col">${t('首項結果','Primary result')}</th></tr></thead><tbody>${rows}</tbody></table>`;
  }

  function translationStatus(status) {
    const isCore = ['zh-TW','en'].includes(language);
    $('translation-wrap').hidden=isCore;
    $('enable-cloud').hidden=isCore || !cloud?.cloudTranslationConfigured() || cloud?.cloudTranslationAllowed();
    if (isCore) return;
    if (status?.state==='translated' || status?.state==='cached') text('translation-note','Machine translation. Formulas, units and reference titles are preserved.');
    else if (status?.state==='translating') text('translation-note','Translating available text…');
    else if (!$('enable-cloud').hidden) text('translation-note','Cloud translation sends public lab text to the configured translation service. Input values and experiment logs stay in this tab.');
    else text('translation-note','Untranslated text remains in English. An on-device or configured translation service is required.');
  }

  function render() {
    locale?.invalidate();
    document.documentElement.lang=language;
    document.documentElement.dir=U.languageDirection?.(language)||'ltr';
    document.title=t('太空任務試算室 · MacGyver V23','Space Mission Lab · MacGyver V23');
    $('lab-language').value=language;
    $('academy-link').href='index.html'+(course?'#project/'+encodeURIComponent(course):'');
    $('academy-link').setAttribute('aria-label',course?t('返回逐步課程','Back to the guided course'):t('返回創新學院','Back to MacGyver Academy'));
    $('world-link').href='experience.html?domain=space'+(course?'&course='+encodeURIComponent(course):'')+'&lang='+language;
    const labels = {
      'world-link':['返回太空工程場景','Back to the space facility'],
      'hero-kicker':['太空與衛星 · 數值實驗','SPACE & SATELLITES · COMPUTATION LAB'],
      'lab-title':['太空任務試算室','Space Mission Lab'],
      'lab-intro':['選擇一種任務模型，調整輸入並檢查物理結果。所有數值是教學假設。可記錄每次條件，將變更及推論帶回逐步課程。','Choose a mission model, change its inputs and check the physics. Values are teaching assumptions. Log each setup and take your results back to the guided lessons.'],
      'models-heading':['選擇任務模型','Choose a mission model'], 'input-heading':['輸入參數','Input parameters'],
      'result-heading':['即時計算結果','Live results'], 'curve-caption':['單一參數的局部變化','Local response to one input'],
      'formula-heading':['計算式','Equations'], 'assumption-heading':['假設與限制','Assumptions and limits'],
      'references-heading':['模型參考資料','Model references'], 'record':['記錄本次試算','Record experiment'],
      'reset':['恢復初始值','Reset inputs'], 'records-title':['試算紀錄','Experiment log'],
      'records-note':['紀錄保留在此分頁的工作階段，最多 50 筆。匯出的 JSON 含輸入、輸出和時間，試算紀錄與課程進度分開。','This tab keeps up to 50 experiments for the session. Export JSON for inputs, outputs and timestamps. Lab records are separate from course progress.'],
      'export':['匯出 JSON','Export JSON']
    };
    for (const [id,label] of Object.entries(labels)) text(id,pick(label));
    text('model-group',pick(current.group));
    text('model-title',pick(current.title));
    text('model-number',`LAB ${String(lab.models.indexOf(current)+1).padStart(2,'0')}`);
    text('model-prompt',pick(current.prompt));
    text('formula',current.formula);
    text('assumption',pick(current.assumption));
    $('references').innerHTML=current.references.map(([title,url])=>`<li><a href="${esc(url)}" target="_blank" rel="noopener noreferrer">${esc(title)}</a></li>`).join('');
    $('models').innerHTML=lab.models.map((model,index)=>`<button type="button" data-model="${model.id}" aria-pressed="${model===current}"><span class="model-id" data-no-translate aria-hidden="true">${String(index+1).padStart(2,'0')}</span>${esc(pick(model.title))}</button>`).join('');
    renderControls();
    compute();
    renderRecords();
    translationStatus();
    if (!['zh-TW','en'].includes(language)) locale?.apply(document.body);
  }

  function selectModel(id,{focus=false,updateHash=false}={}) {
    const model=modelFor(id);
    if (!model || model===current) return;
    if (frame) { cancelAnimationFrame(frame);frame=0; }
    current=model;values=lab.defaults(id);recordMessage='';
    if (updateHash) {
      try { history.replaceState(null,'','#'+id); } catch { location.hash=id; }
    }
    render();
    if (focus) $('models').querySelector(`[data-model="${id}"]`)?.focus({preventScroll:true});
  }

  function initTranslator(create) {
    if (!create) return;
    locale?.invalidate();
    locale = create({getLanguage:()=>language,getTranslationAvailable:()=>hostedTranslation,getCloudAllowed:()=>true,onStatus:translationStatus,onDictionary:()=>locale?.apply(document.body)});
  }
  async function configureTranslation() {
    if (location.protocol==='file:') return;
    try {
      const [module,worker] = await Promise.all([import('./locale.js'),import('./mentor-cloud-v23.js')]);
      cloud=worker;
      initTranslator(module.createLocaleController);
      translationStatus();
      if (!['zh-TW','en'].includes(language)) locale?.apply(document.body);
    } catch { /* Static mirrors may serve the bundled controller only. */ }
    if (window.MG_RUNTIME?.isHosted?.() || window.MG_CONFIG?.accountMode==='hosted') {
      try {
        const response=await fetch('/api/me',{credentials:'same-origin'}), me=response.ok?await response.json():{};
        hostedTranslation=!!me.user&&!!(me.translationAvailable??me.aiAvailable);
        if (hostedTranslation && !['zh-TW','en'].includes(language)) locale?.apply(document.body);
      } catch { /* Translation remains optional. */ }
    }
  }

  $('lab-language').replaceChildren(...supported.map(code=>{
    let label=code;
    try { label=new Intl.DisplayNames([code],{type:'language'}).of(code)||code; } catch { /* Old browser. */ }
    return new Option(code==='zh-TW'?'繁體中文':code==='en'?'English':label,code);
  }));
  $('lab-language').addEventListener('change',event=>{
    language=resolve(event.target.value);recordMessage='';
    try { localStorage.setItem('mg-language',language); } catch { /* The selected locale still applies to this page. */ }
    render();
  });
  $('enable-cloud').addEventListener('click',()=>{
    if (cloud?.allowCloudTranslation()) {
      translationStatus();
      locale?.apply(document.body);
    }
  });
  $('models').addEventListener('click',event=>{
    const button=event.target.closest('[data-model]');
    if (button) selectModel(button.dataset.model,{focus:true,updateHash:true});
  });
  window.addEventListener('hashchange',()=>selectModel(location.hash.slice(1)));
  $('reset').addEventListener('click',()=>{
    values=lab.defaults(current.id);recordMessage='';render();
  });
  $('record').addEventListener('click',()=>{
    const result=compute();
    if (!result) return;
    records.push({model:current.id,inputs:{...values},result,at:new Date().toISOString()});
    records=records.slice(-50);
    recordMessage=t('已記錄輸入與計算結果。','Inputs and results recorded.');
    try { sessionStorage.setItem(recordKey,JSON.stringify(records)); }
    catch { recordMessage=t('目前紀錄保留在此頁，離開前請匯出。','Records stay on this page. Export before leaving.'); }
    renderRecords();
  });
  $('export').addEventListener('click',()=>{
    if (!records.length) return;
    const blob = new Blob([JSON.stringify({format:'macgyver-space-lab-v23',courseId:course||null,records},null,2)],{type:'application/json'});
    const url=URL.createObjectURL(blob), link=document.createElement('a');
    link.href=url;link.download='MacGyver_V23_Space_Experiments.json';
    document.body.append(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
  });
  initTranslator(U.createLocaleController);
  render();
  void configureTranslation();
})();
