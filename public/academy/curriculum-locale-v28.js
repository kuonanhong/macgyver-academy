/* V28 whole-content language controls. No location lookup, API keys, or network
 * translation until a configured route is available. UI dictionaries and full
 * course translation are reported separately. Works with classic file bundles. */
(function(root){
  'use strict';
  const U=root.MG_CAMPAIGN_UTILS||{};
  const supported=Object.freeze(Array.from(U.SUPPORTED_LANGUAGES||U.supportedLanguages||['zh-TW','en']));
  const core=language=>language==='zh-TW'||language==='en';
  const label=code=>{try{return new Intl.DisplayNames([code],{type:'language'}).of(code)||code;}catch{return code;}};
  function voiceFor(language,voices=[]){
    const canonical=value=>String(value||'').replaceAll('_','-').toLowerCase();
    const requested=canonical(language),base=requested.split('-')[0];
    const chinese=code=>/hant|tw|hk|mo/.test(code)?'hant':/hans|cn|sg/.test(code)?'hans':'';
    const compatible=voice=>canonical(voice.lang).split('-')[0]===base&&
      (base!=='zh'||!chinese(requested)||chinese(canonical(voice.lang))===chinese(requested));
    return voices.find(v=>canonical(v.lang)===requested)||voices.find(v=>compatible(v)&&v.localService)||voices.find(compatible)||null;
  }
  function chunks(value,size=220){
    const out=[];let remaining=String(value||'').trim();
    while(remaining.length>size){
      const piece=remaining.slice(0,size+1);
      let stop=Math.max(piece.lastIndexOf('\n'),piece.lastIndexOf('. '),piece.lastIndexOf('。'),piece.lastIndexOf('！'),piece.lastIndexOf('? '));
      if(stop<size/3)stop=piece.lastIndexOf(' ');
      if(stop<size/3)stop=size;else stop++;
      if(/[\uD800-\uDBFF]/.test(remaining[stop-1]))stop--;
      out.push(remaining.slice(0,stop).trim());remaining=remaining.slice(stop).trim();
    }
    if(remaining)out.push(remaining);return out;
  }
  function create({select,status,cloudButton,deviceButton,urlPreference=null,onChange=()=>{},retryButton=null,speakButton=null,stopButton=null}={}){
    const doc=root.document;
    if(!select||!status)throw Error('V28 language controls require select and status elements.');
    const handlers=[];
    const listen=(target,event,fn,options)=>{target?.addEventListener?.(event,fn,options);handlers.push(()=>target?.removeEventListener?.(event,fn,options));};
    const read=()=>{try{return root.localStorage.getItem('mg-language')||'auto';}catch{return 'auto';}};
    const valid=value=>typeof value==='string'&&(value==='auto'||/^[a-z]{2,3}(?:[-_][a-z0-9]{2,8})*$/i.test(value)&&
      (supported.some(code=>code.split('-')[0]===value.split(/[-_]/)[0].toLowerCase())||['iw','in','tl','nb','nn'].includes(value.split(/[-_]/)[0].toLowerCase())));
    const resolve=value=>U.resolveSupportedLanguage?.(value,root.navigator,supported)||'en';
    const normalize=value=>valid(value)?value==='auto'?'auto':resolve(value):'auto';
    let preference=normalize(valid(urlPreference)?urlPreference:read()),language=resolve(preference),lastRoot=null,hosted=false,latest=null,controller=null,disposed=false,voiceEpoch=0,speaking=false;
    status.setAttribute('data-no-translate','');status.setAttribute('role','status');status.setAttribute('aria-live','polite');
    select.replaceChildren();
    for(const code of ['auto',...supported]){
      const option=doc.createElement('option');option.value=code;option.textContent=code==='auto'?'Auto · 瀏覽器 / Browser':code==='zh-TW'?'繁體中文':code==='en'?'English':label(code);select.append(option);
    }
    select.setAttribute('data-no-translate','');
    // Existing pages may provide buttons; otherwise add accessible narration
    // and retry controls beside the coverage status without changing their API.
    let tools=null;
    if(status.parentNode?.append&&(!retryButton||!speakButton||!stopButton)){
      tools=doc.createElement('div');tools.className='locale-tools-v28';tools.setAttribute('data-no-translate','');
      function button(action){const b=doc.createElement('button');b.type='button';b.dataset.localeAction=action;tools.append(b);return b;}
      retryButton=retryButton||button('retry');speakButton=speakButton||button('speak');stopButton=stopButton||button('stop');status.parentNode.append(tools);
    }
    function local(a,b){return language==='zh-TW'?a:b;}
    function controls(){
      if(cloudButton)cloudButton.hidden=core(language)||!U.cloudTranslationConfigured?.()||!!U.cloudTranslationAllowed?.();
      if(deviceButton)deviceButton.hidden=core(language)||!root.Translator?.create;
      if(retryButton){retryButton.hidden=core(language);retryButton.textContent=local('重試正文翻譯','Retry content translation');retryButton.disabled=latest?.state==='translating';}
      if(speakButton){speakButton.textContent=local('朗讀目前正文','Read visible content');speakButton.disabled=!root.speechSynthesis||!root.SpeechSynthesisUtterance||speaking;}
      if(stopButton){stopButton.textContent=local('停止朗讀','Stop reading');stopButton.hidden=!speaking;}
    }
    function describe(value){
      if(disposed||value?.language&&value.language!==language)return;
      latest=value||{state:core(language)?'core':'unavailable',language,total:0,translated:0,pending:0};
      status.dataset.state=latest.state||'unavailable';status.dataset.language=language;
      const total=Math.max(0,Number(latest.total)||0),done=Math.min(total,Math.max(0,Number(latest.translated)||0));
      const pending=Number.isFinite(latest.pending)?latest.pending:Math.max(0,total-done);
      if(core(language))status.textContent=local(
        `完整繁體中文與英文原創內容；可選 ${supported.length} 個語系。其他語系需要裝置或已設定的翻譯服務，並逐段顯示涵蓋率。`,
        `Complete authored Traditional Chinese and English; ${supported.length} language targets. Other targets require device or configured translation; coverage is reported per visible section.`);
      else{
        const count=total?`${done} / ${total} public text fragments translated. `:'';
        const prefix=label(language)+' · '+count;
        if(latest.state==='translating')status.textContent=prefix+'Translating visible lesson content…';
        else if(total>0&&pending===0&&['translated','cached'].includes(latest.state))status.textContent=prefix+'Machine translation. Formulas and source references remain unchanged; verify technical meaning against English or Chinese.';
        else status.textContent=prefix+'Remaining content stays in English. This language needs a supported device translator or configured service. Your notes, questions and form values are excluded.';
      }
      controls();
    }
    function stop(){voiceEpoch++;speaking=false;root.speechSynthesis?.cancel?.();controls();}
    function apply(node=lastRoot){
      if(disposed)return Promise.resolve({state:'disposed'});
      if(node)lastRoot=node;
      doc.documentElement.lang=language;doc.documentElement.dir=U.languageDirection?.(language)||'ltr';select.value=preference;
      describe();
      if(controller&&lastRoot)return controller.apply(lastRoot);
      return Promise.resolve(latest);
    }
    controller=U.createLocaleController?.({getLanguage:()=>language,getTranslationAvailable:()=>hosted,getCloudAllowed:()=>true,onStatus:describe,onDictionary:loaded=>{if(loaded===language&&lastRoot&&!disposed)void apply(lastRoot);}});
    function change(value,{save=false,notify=true}={}){
      stop();preference=normalize(value);language=resolve(preference);controller?.invalidate();select.value=preference;
      if(save)try{root.localStorage.setItem('mg-language',preference);}catch{}
      if(notify)onChange({language,preference});
    }
    function narrate(node=lastRoot){
      stop();
      if(!root.speechSynthesis||!root.SpeechSynthesisUtterance)return false;
      if(!core(language)&&!(latest?.total>0&&latest?.pending===0&&latest?.translated===latest?.total)){
        status.textContent='Reading is paused because this section is not fully translated. Choose English / 繁體中文 or finish translation first.';return false;
      }
      const voice=voiceFor(language,root.speechSynthesis.getVoices?.()||[]);
      if(!voice){status.textContent=local('裝置沒有此語系的朗讀語音；可在系統設定安裝語音，或繼續閱讀文字。','No matching voice is installed on this device. Install a system voice or continue reading the text.');return false;}
      const text=U.publicTextSnapshot?.(node,{maxCharacters:24000})||'';
      const segments=chunks(text);if(!segments.length)return false;
      const epoch=voiceEpoch;let index=0;speaking=true;controls();
      const next=()=>{
        if(epoch!==voiceEpoch||disposed)return;
        if(index>=segments.length){speaking=false;controls();return;}
        const utterance=new root.SpeechSynthesisUtterance(segments[index++]);utterance.lang=language;utterance.voice=voice;utterance.rate=0.95;
        utterance.onend=next;utterance.onerror=()=>{if(epoch===voiceEpoch){speaking=false;controls();status.textContent=local('朗讀已停止；文字仍可閱讀。','Speech stopped; lesson text remains available.');}};
        root.speechSynthesis.speak(utterance);
      };
      next();return true;
    }
    listen(select,'change',event=>change(event.target.value,{save:true}));
    listen(root,'languagechange',()=>{if(preference==='auto')change('auto');});
    listen(root,'storage',event=>{if(event.key==='mg-language'||event.key===null)change(event.key===null?'auto':event.newValue||'auto');});
    listen(cloudButton,'click',()=>{if(U.allowCloudTranslation?.())void apply();else describe();});
    listen(deviceButton,'click',async()=>{
      if(deviceButton)deviceButton.disabled=true;
      const requested=language;
      try{
        const translator=await U.onDeviceTranslator?.(requested,{userActivated:true,onProgress:fraction=>{
          if(requested===language)status.textContent=`${label(language)} · Preparing device translation${fraction==null?'…':' '+Math.round(fraction*100)+'%'}; course text remains available.`;
        }});
        if(requested!==language||disposed)return;
        await apply();
        if(!translator&&latest?.pending)status.textContent=label(language)+' · Device translation is unavailable for this language pair. Use English / 繁體中文 or a configured service.';
      }finally{if(deviceButton)deviceButton.disabled=false;}
    });
    listen(retryButton,'click',()=>void apply());listen(speakButton,'click',()=>narrate());listen(stopButton,'click',stop);
    listen(doc,'toggle',event=>{if(event.target?.tagName==='DETAILS'&&event.target.open&&lastRoot?.contains?.(event.target))void apply();},true);
    listen(root.speechSynthesis,'voiceschanged',controls);
    if(root.location?.protocol!=='file:'&&(root.MG_RUNTIME?.isHosted?.()||root.MG_CONFIG?.accountMode==='hosted')){
      Promise.resolve(root.fetch('/api/me',{credentials:'same-origin'})).then(response=>response.ok?response.json():{}).then(me=>{if(disposed)return;hosted=!!me.user&&!!(me.translationAvailable??me.aiAvailable);if(hosted&&lastRoot)void apply();}).catch(()=>{});
    }
    controls();
    return Object.freeze({get language(){return language;},get preference(){return preference;},get status(){return latest;},apply,narrate,stop,
      invalidate:()=>controller?.invalidate(),readUrl:value=>{if(valid(value))change(value,{notify:false});},
      exportCache:()=>controller?.exportCache(language),importCache:pack=>controller?.importCache(pack),
      dispose:()=>{stop();disposed=true;controller?.invalidate();handlers.forEach(remove=>remove());tools?.remove?.();}
    });
  }
  root.MG_CURRICULUM_LOCALE_V28=Object.freeze({supported,create,voiceFor,chunks});
})(window);
