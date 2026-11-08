/* Shared locale controller for the public V26 register; works with classic
 * campaign utilities at file://. Course metadata is public; search values and
 * the learner's last-opened link are explicitly excluded from translation. */
(function(root){
  'use strict';
  const supported=Object.freeze('zh-TW en zh-CN ja ko es fr de pt it nl ru uk pl cs sk sl hr sr bg ro hu el tr ar he fa ur hi bn ta te mr gu kn ml pa ne si th vi id ms fil km lo my mn kk uz az ka hy sw am ha yo ig zu af so sv no da fi is et lv lt ga cy mt sq mk bs eu gl ca eo'.split(' '));
  const supportedBases=new Set(supported.map(code=>code.split('-')[0]));
  function create({select,status,cloudButton,deviceButton,urlPreference=null,onChange=()=>{}}){
    const U=root.MG_CAMPAIGN_UTILS||{},doc=root.document;
    const stored=()=>{try{return root.localStorage.getItem('mg-language')||'auto';}catch{return 'auto';}};
    const valid=value=>typeof value==='string'&&(value==='auto'||/^[a-z]{2,3}(?:[-_][a-z0-9]{2,8})*$/i.test(value)&&(supportedBases.has(value.split(/[-_]/)[0].toLowerCase())||['iw','in','tl','nb','nn'].includes(value.split(/[-_]/)[0].toLowerCase())));
    const resolve=value=>U.resolveSupportedLanguage?.(value,root.navigator,supported)||(/^zh/i.test(value==='auto'?root.navigator?.language:value)?'zh-TW':supported.includes(value)?value:'en');
    const normalize=value=>valid(value)?value==='auto'?'auto':resolve(value):'auto';
    let preference=normalize(valid(urlPreference)?urlPreference:stored()),language=resolve(preference),lastRoot=null,hosted=false,latest=null,controller;
    function label(code){try{return new Intl.DisplayNames([code],{type:'language'}).of(code)||code;}catch{return code;}}
    select.replaceChildren();
    for(const code of ['auto',...supported]){
      const option=doc.createElement('option');option.value=code;option.textContent=code==='auto'?'Auto · 瀏覽器 / Browser':code==='zh-TW'?'繁體中文':code==='en'?'English':label(code);select.append(option);
    }
    select.setAttribute('data-no-translate','');
    function describe(value){
      if(value?.language&&value.language!==language)return;
      latest=value||{state:['zh-TW','en'].includes(language)?'core':'unavailable',language,total:0,translated:0,pending:0};
      if(latest.language&&latest.language!==language)return;
      const core=language==='zh-TW'||language==='en';
      cloudButton.hidden=core||!U.cloudTranslationConfigured?.()||!!U.cloudTranslationAllowed?.();
      deviceButton.hidden=core||!root.Translator?.create;
      status.dataset.state=latest.state||'unavailable';status.dataset.language=language;
      if(core){status.textContent=language==='zh-TW'?'繁體中文與英文為完整原創內容。可選擇 79 個語系；其他語系依字典、裝置或已設定的服務翻譯。':'Complete authored text is available in Traditional Chinese and English. Choose among 79 language targets; other languages use dictionaries, device translation or a configured service.';return;}
      const total=Math.max(0,Number(latest.total)||0),done=Math.min(total,Math.max(0,Number(latest.translated)||0));
      const pending=Number.isFinite(latest.pending)?latest.pending:Math.max(0,total-done);
      const count=total?`${done} / ${total} public text fragments translated. `:'';
      const prefix=`${label(language)} · `;
      if(latest.state==='translating')status.textContent=prefix+count+'Translating available public text…';
      else if(total&&pending===0&&['translated','cached'].includes(latest.state))status.textContent=prefix+count+'Machine translation; review against the authored Chinese or English text.';
      else status.textContent=prefix+count+'Remaining text stays in English. A supported device translator or configured translation service is required. Search values and your last-opened course are not sent.';
    }
    function apply(node=lastRoot){
      if(node)lastRoot=node;
      doc.documentElement.lang=language;doc.documentElement.dir=U.languageDirection?.(language)||'ltr';select.value=preference;
      describe();
      if(controller&&lastRoot)return controller.apply(lastRoot);
      return Promise.resolve(latest);
    }
    controller=U.createLocaleController?.({getLanguage:()=>language,getTranslationAvailable:()=>hosted,getCloudAllowed:()=>true,onStatus:describe,onDictionary:loaded=>{if(loaded===language&&lastRoot)void apply(lastRoot);}});
    function change(value,{save=false,notify=true}={}){
      preference=normalize(value);language=resolve(preference);controller?.invalidate();
      select.value=preference;
      if(save)try{root.localStorage.setItem('mg-language',preference);}catch{/* Page preference still works. */}
      if(notify)onChange({language,preference});
    }
    select.addEventListener('change',event=>change(event.target.value,{save:true}));
    root.addEventListener('languagechange',()=>{if(preference==='auto')change('auto');});
    root.addEventListener('storage',event=>{if(event.key==='mg-language'||event.key===null)change(event.key===null?'auto':event.newValue||'auto');});
    cloudButton.addEventListener('click',()=>{if(U.allowCloudTranslation?.())void apply();else describe();});
    deviceButton.addEventListener('click',async()=>{
      deviceButton.disabled=true;
      try{await U.onDeviceTranslator?.(language,{userActivated:true});await apply();}
      finally{deviceButton.disabled=false;}
    });
    if(root.location.protocol!=='file:'&&(root.MG_RUNTIME?.isHosted?.()||root.MG_CONFIG?.accountMode==='hosted')){
      Promise.resolve(root.fetch('/api/me',{credentials:'same-origin'})).then(response=>response.ok?response.json():{}).then(me=>{hosted=!!me.user&&!!(me.translationAvailable??me.aiAvailable);if(hosted&&lastRoot)void apply();}).catch(()=>{/* Device/cache support remains available. */});
    }
    return Object.freeze({get language(){return language;},get preference(){return preference;},get status(){return latest;},apply,invalidate:()=>controller?.invalidate(),readUrl:value=>{if(valid(value))change(value,{notify:false});}});
  }
  root.MG_CURRICULUM_LOCALE_V26=Object.freeze({supported,create});
})(window);
