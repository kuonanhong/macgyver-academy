/** V10 personal workspace. Preferences stay in this browser, separated by profile.
 * No account data, voice list or preferences are sent to another service.
 * Remote system voices may use their own provider; the chooser labels them.
 */
const PREFIX = 'mg-workspace-v10:';
export const DEFAULT_PREFERENCES = Object.freeze({theme:'system',layout:'comfortable',accent:'forest',fontScale:1,sidebar:'full',voiceURI:'',voiceLanguage:'follow',voiceGender:'any',voiceStyle:'professional',rate:.95,pitch:1});
/* Narration "personalities". The Web Speech API exposes only rate and pitch, so
 * a style is a rate/pitch preset applied to the chosen device voice. */
export const VOICE_STYLES = Object.freeze({
  professional:{rate:.95,pitch:1,zh:'專業講師（清楚、穩定）',en:'Professional instructor (clear, steady)'},
  chief:{rate:.88,pitch:.85,zh:'沉穩總工程師（低沉、從容）',en:'Calm chief engineer (lower, unhurried)'},
  broadcast:{rate:1,pitch:.95,zh:'新聞播報（俐落、正式）',en:'Broadcast (crisp, formal)'},
  lively:{rate:1.08,pitch:1.15,zh:'活潑助教（明亮、輕快）',en:'Lively assistant (bright, brisk)'},
  clear:{rate:.78,pitch:1,zh:'清晰慢速（初學者）',en:'Clear and slow (beginners)'},
  custom:{zh:'自訂語速與音高',en:'Custom rate and pitch'}
});
const FEMALE=/samantha|karen|moira|tessa|victoria|fiona|allison|\bava\b|susan|zoe|kate|serena|veena|mei-?jia|sin-?ji|ting-?ting|kyoko|yuna|am[eé]lie|\banna\b|alice|paulina|m[oó]nica|joana|luciana|ellen|\bsara\b|nora|zuzana|ioana|milena|melina|yelda|laura|carmit|lekha|damayanti|kanya|\blinh\b|zira|hazel|hanhan|yating|huihui|haruka|ayumi|heami|hsiaochen|hsiaoyu|xiaoxiao|xiaoyi|xiaohan|nanami|sunhi|jenny|\baria\b|sonia|libby|natasha|clara|elvira|denise|katja|isabella|francisca|female|女/i;
const MALE=/\balex\b|daniel|\bfred\b|\btom\b|oliver|aaron|arthur|gordon|rishi|thomas|xander|yuri|jorge|diego|\bjuan\b|\bluca\b|\breed\b|rocko|\beddy\b|grandpa|ralph|david|\bmark\b|george|zhiwei|kangkang|ichiro|yunjhe|yunxi|yunyang|yunjian|keita|injoon|\bguy\b|\bryan\b|christopher|\beric\b|william|henri|conrad|alvaro|\bmale\b|男/i;
/** Best-effort voice gender from well-known system voice names; 'unknown' when unsure. */
export function voiceGender(voice){const name=String(voice?.name||'');if(/\bfemale\b|女/i.test(name))return 'female';if(/\bmale\b|男/i.test(name))return 'male';if(/^google\s/i.test(name))return 'female';if(FEMALE.test(name))return 'female';if(MALE.test(name))return 'male';return 'unknown';}
const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const locale = value => String(value || '').replaceAll('_','-').toLowerCase();
const base = value => locale(value).split('-')[0];
const bounded = (value,min,max,fallback) => typeof value === 'number' && Number.isFinite(value) ? Math.max(min,Math.min(max,value)) : fallback;
const languageCode = value => value === 'follow' || /^[a-z]{2,3}(?:-[A-Za-z0-9]{2,8}){0,3}$/.test(value || '') ? value : 'follow';
export function normalizePreferences(value) {
  const input = value && typeof value === 'object' && !Array.isArray(value) ? value : {};
  return {theme:['system','light','dark'].includes(input.theme)?input.theme:'system',layout:['comfortable','compact','focus'].includes(input.layout)?input.layout:'comfortable',accent:['forest','ocean','amber','violet','graphite'].includes(input.accent)?input.accent:'forest',fontScale:[0.9,1,1.1,1.2].includes(input.fontScale)?input.fontScale:1,sidebar:['full','compact','hidden'].includes(input.sidebar)?input.sidebar:'full',voiceGender:['any','female','male'].includes(input.voiceGender)?input.voiceGender:'any',voiceStyle:Object.keys(VOICE_STYLES).includes(input.voiceStyle)?input.voiceStyle:'professional',voiceURI:typeof input.voiceURI==='string'?input.voiceURI.slice(0,500):'',voiceLanguage:languageCode(input.voiceLanguage),rate:bounded(input.rate,.6,1.4,.9),pitch:bounded(input.pitch,.6,1.4,1)};
}
export function preferenceKey(profileId='guest') { return PREFIX + encodeURIComponent(String(profileId || 'guest').slice(0,300)); }
export function choosePersonalVoice(voices,language,voiceURI='',gender='any') {
  const all = Array.from(voices || []).filter(voice => base(voice.lang) === base(language));
  const explicit = all.find(voice => voiceURI && voice.voiceURI === voiceURI);
  if (explicit) return explicit;
  const gendered = gender === 'any' ? all : all.filter(voice => voiceGender(voice) === gender);
  const matching = gendered.length ? gendered : all;
  return matching.find(voice => locale(voice.lang) === locale(language) && voice.localService) || matching.find(voice => locale(voice.lang) === locale(language)) || matching.find(voice => voice.default) || matching[0] || null;
}

export function createPersonalization(options={}) {
  const document = options.document || globalThis.document;
  const environment = options.environment || document?.defaultView || globalThis;
  let storage;
  try { storage = options.storage === undefined ? environment.localStorage : options.storage; } catch { storage = null; }
  const language = () => options.getLanguage?.() || document?.documentElement?.lang || 'en';
  const zh = () => base(language()) === 'zh';
  const words = (a,b) => zh()?a:b;
  const synth = options.speechSynthesis || environment.speechSynthesis;
  let profileId='', preferences={...DEFAULT_PREFERENCES}, saved=true, dialog=null, speaking=null, opener=null;
  const media = environment.matchMedia?.('(prefers-color-scheme: dark)');
  const voices = () => {try{return synth?.getVoices?.() || []}catch{return []}};
  const notify = () => options.onChanged?.({...preferences},{profileId,saved});
  const apply = () => {
    const root=document?.documentElement;if(!root)return;
    root.dataset.theme=preferences.theme==='system'?(media?.matches?'dark':'light'):preferences.theme;
    root.dataset.themePreference=preferences.theme;root.dataset.layout=preferences.layout;root.dataset.accent=preferences.accent;root.dataset.sidebar=preferences.sidebar;root.style?.setProperty?.('--mg-font-scale',String(preferences.fontScale));
    const themeColor=document.querySelector?.('meta[name="theme-color"]');if(themeColor)themeColor.content=root.dataset.theme==='dark'?'#111b20':'#f5f7f8';
  };
  const persist = () => {try {if(!storage)throw new Error('storage unavailable');storage.setItem(preferenceKey(profileId),JSON.stringify(preferences));saved=true}catch{saved=false}apply();notify();return saved};
  const stopVoice = () => {if(speaking){speaking.onend=null;speaking.onerror=null;speaking=null;try{synth?.cancel()}catch{}}};
  const status = message => {const output=dialog?.querySelector('[data-preference-status]');if(output)output.textContent=message};
  const describeSaved = () => saved?words('已保存至此裝置的目前會員／學習檔案。','Saved on this device for the current member / learning profile.'):words('此瀏覽器無法保存設定；本次開啟仍有效，請匯出備份。','This browser cannot persist preferences. They remain active for this session; export a backup.');
  const syncProfile = () => {
    const next=String(options.getProfileId?.() || 'guest');
    if(next!==profileId){stopVoice();profileId=next;try{preferences=normalizePreferences(JSON.parse(storage?.getItem(preferenceKey(profileId)) || 'null'));saved=!!storage}catch{preferences={...DEFAULT_PREFERENCES};saved=false}apply();if(dialog?.open)renderDialog()}
    const button=document?.getElementById?.('preferencesButton');if(button){button.title=words('個人工作室與語音','Personal workspace and voice');button.setAttribute('aria-label',button.title)}
    return {...preferences};
  };
  const getNarrationLanguage = (fallback=language()) => preferences.voiceLanguage==='follow'?fallback:preferences.voiceLanguage;
  const getSpeechOptions = (spokenLanguage=getNarrationLanguage()) => {
    const voice=choosePersonalVoice(voices(),spokenLanguage,preferences.voiceURI,preferences.voiceGender);
    // When no voice of the requested gender exists, approximate with pitch.
    const missing=preferences.voiceGender!=='any'&&!preferences.voiceURI&&voice&&voiceGender(voice)!==preferences.voiceGender;
    const pitch=missing?Math.max(.5,Math.min(2,preferences.pitch*(preferences.voiceGender==='male'?.82:1.18))):preferences.pitch;
    return {language:spokenLanguage,voiceURI:voice?.voiceURI || '',rate:preferences.rate,pitch,genderApproximated:!!missing};
  };
  const update = value => {preferences=normalizePreferences({...preferences,...value});persist();return {...preferences}};
  const voiceOptions = () => {
    const spokenLanguage=getNarrationLanguage(),list=voices().filter(voice=>base(voice.lang)===base(spokenLanguage));
    return `<option value="">${words('依講解語言自動選擇','Automatically match narration language')}</option>${list.map(voice=>`<option value="${escape(voice.voiceURI)}" ${voice.voiceURI===preferences.voiceURI?'selected':''}>${escape(voice.name)} · ${escape(voice.lang)} · ${({female:words('女聲','female'),male:words('男聲','male'),unknown:words('未標示','unlabelled')})[voiceGender(voice)]} · ${voice.localService?words('裝置語音','device voice'):words('網路語音','network voice')}</option>`).join('')}`;
  };
  const refreshVoices = () => {
    const select=dialog?.querySelector('[data-pref="voiceURI"]');if(!select)return;select.innerHTML=voiceOptions();
    const text=dialog.querySelector('[data-voice-availability]'),count=voices().filter(voice=>base(voice.lang)===base(getNarrationLanguage())).length;
    text.textContent=count?words(`本裝置提供 ${count} 個相符語音。`,`This device provides ${count} matching voices.`):words('本裝置尚無相符語音。仍可逐段阅读；請在系統中安裝此語言的語音，或使用其他講解語言。','No matching voice is available. Read section by section, install this language’s voice in the operating system, or select another narration language.');
  };
  const renderDialog = () => {
    if(!dialog)return;
    const list=[...new Set(['zh-TW','en','zh-CN','ja','ko','es','fr','de','pt','it',language(),...voices().map(voice=>voice.lang)].filter(code=>languageCode(code)!=='follow'))].sort((a,b)=>a.localeCompare(b));
    dialog.innerHTML=`<div class="dialog-head"><div><span class="eyebrow">PERSONAL WORKSPACE</span><h2>${words('我的工作室','My workspace')}</h2></div><button class="icon-btn" data-preference-close type="button" aria-label="${words('關閉','Close')}">×</button></div><p class="preference-profile" data-no-translate>${escape(options.getProfileName?.() || profileId)}</p><p class="subtext">${words('外觀與聲音設定依目前會員／學習檔案，分別存於此瀏覽器。可匯出後在另一部裝置匯入。','Appearance and voice preferences are saved separately for this member / profile in this browser. Export and import them on another device.')}</p><form data-preference-form><fieldset><legend>${words('桌面外觀','Workspace appearance')}</legend><div class="preference-grid"><label>${words('色彩主題','Color theme')}<select data-pref="theme">${[['system',words('跟隨系統','Follow system')],['light',words('淺色','Light')],['dark',words('深色','Dark')]].map(([id,title])=>`<option value="${id}" ${preferences.theme===id?'selected':''}>${title}</option>`).join('')}</select></label><label>${words('閱讀佈局','Reading layout')}<select data-pref="layout">${[['comfortable',words('舒適・較多留白','Comfortable · more space')],['compact',words('緊湊・更多內容','Compact · denser content')]].map(([id,title])=>`<option value="${id}" ${preferences.layout===id?'selected':''}>${title}</option>`).join('')}</select></label><label>${words('強調色','Accent colour')}<select data-pref="accent">${[['forest',words('森林綠（預設）','Forest green (default)')],['ocean',words('海洋藍','Ocean blue')],['amber',words('琥珀金','Amber')],['violet',words('科技紫','Violet')],['graphite',words('石墨灰','Graphite')]].map(([id,title])=>`<option value="${id}" ${preferences.accent===id?'selected':''}>${title}</option>`).join('')}</select></label><label>${words('字體大小','Text size')}<select data-pref="fontScale">${[[0.9,words('小','Small')],[1,words('標準','Standard')],[1.1,words('大','Large')],[1.2,words('特大','Extra large')]].map(([id,title])=>`<option value="${id}" ${preferences.fontScale===id?'selected':''}>${title}</option>`).join('')}</select></label><label>${words('側邊欄','Sidebar')}<select data-pref="sidebar">${[['full',words('完整（圖示＋文字）','Full (icons + labels)')],['compact',words('精簡（只顯示圖示）','Compact (icons only)')],['hidden',words('隱藏（專注模式，按 ☰ 開啟）','Hidden (focus mode, open with ☰)')]].map(([id,title])=>`<option value="${id}" ${preferences.sidebar===id?'selected':''}>${title}</option>`).join('')}</select></label></div></fieldset><fieldset><legend>${words('師傅講解聲音','Mentor narration')}</legend><div class="preference-grid"><label>${words('聲音性別','Voice gender')}<select data-pref="voiceGender">${[['any',words('不限','Any')],['female',words('女聲','Female')],['male',words('男聲','Male')]].map(([id,title])=>`<option value="${id}" ${preferences.voiceGender===id?'selected':''}>${title}</option>`).join('')}</select></label><label>${words('講解風格／專業度','Narration style')}<select data-pref="voiceStyle">${Object.entries(VOICE_STYLES).map(([id,v])=>`<option value="${id}" ${preferences.voiceStyle===id?'selected':''}>${words(v.zh,v.en)}</option>`).join('')}</select></label></div><label>${words('講解語言','Narration language')}<select data-pref="voiceLanguage" data-no-translate><option value="follow" ${preferences.voiceLanguage==='follow'?'selected':''}>${words('跟隨頁面／瀏覽器語言','Follow page / browser language')}</option>${list.map(code=>`<option value="${escape(code)}" ${preferences.voiceLanguage===code?'selected':''}>${escape(code)}</option>`).join('')}</select></label><label>${words('選擇聲音','Choose a voice')}<select data-pref="voiceURI" data-no-translate>${voiceOptions()}</select></label><p class="subtext" data-voice-availability></p><p class="preference-note">${words('可依聲音名稱試聽，挑選喜歡的男聲或女聲。瀏覽器不提供一致的性別／專業度資料；音高與語速可以調整，實際聲線以裝置提供為準。網路語音可能將朗讀文字交給系統的語音服務。','Preview named voices to find the sound you prefer, including male or female voices when available. Browsers do not standardize gender or expertise labels. Pitch and speed are adjustable; actual voices depend on your device. Network voices may send narration text to the operating system’s speech provider.')}</p><div class="preference-presets" role="group" aria-label="${words('講解節奏預設','Narration pace presets')}"><button type="button" class="chip" data-voice-preset="careful">${words('清楚慢講','Careful pace')}</button><button type="button" class="chip" data-voice-preset="natural">${words('自然節奏','Natural pace')}</button><button type="button" class="chip" data-voice-preset="brisk">${words('快速複習','Quick review')}</button></div><div class="preference-grid"><label>${words('語速','Speed')} <output data-pref-output="rate">${preferences.rate.toFixed(2)}×</output><input type="range" min="0.6" max="1.4" step="0.05" value="${preferences.rate}" data-pref="rate"></label><label>${words('音高','Pitch')} <output data-pref-output="pitch">${preferences.pitch.toFixed(2)}</output><input type="range" min="0.6" max="1.4" step="0.05" value="${preferences.pitch}" data-pref="pitch"></label></div><div class="dialog-actions"><button type="button" class="button" data-voice-test>${words('▶ 試聽聲音','▶ Preview voice')}</button><button type="button" class="button light" data-voice-stop>${words('停止試聽','Stop preview')}</button></div><p class="preference-note">${words('跟隨頁面時採用手動選擇或瀏覽器語言偏好，不以所在國家或 GPS 猜測。繁中／英文以外的講解須有已設定的翻譯服務；缺少翻譯或相符語音時保留文字閱讀。新的聲音設定會套用於下一段講解。','Follow page uses your manual choice or browser language preferences, not country or GPS. Narration outside the core Chinese / English languages needs a configured translation service. Missing translations or voices leave text available. New voice settings apply to the next narrated section.')}</p></fieldset><div class="dialog-actions"><button type="button" class="button light" data-preference-export>${words('匯出設定','Export preferences')}</button><label class="button light preference-import">${words('匯入設定','Import preferences')}<input type="file" accept="application/json,.json" data-preference-import></label><button type="button" class="text-link" data-preference-reset>${words('恢復預設','Restore defaults')}</button></div><p data-preference-status role="status" aria-live="polite">${describeSaved()}</p></form>`;
    dialog.querySelector('[data-preference-close]').onclick=()=>dialog.close();
    dialog.querySelector('[data-preference-form]').onsubmit=event=>event.preventDefault();
    dialog.querySelectorAll('[data-pref]').forEach(input=>{input.addEventListener(input.type==='range'?'input':'change',()=>{const key=input.dataset.pref;const raw=input.type==='range'||key==='fontScale'?Number(input.value):input.value;const style=key==='voiceStyle'&&VOICE_STYLES[raw]?.rate?{rate:VOICE_STYLES[raw].rate,pitch:VOICE_STYLES[raw].pitch}:{};const manual=key==='rate'||key==='pitch'?{voiceStyle:'custom'}:{};update({[key]:raw,...style,...manual,...(key==='voiceLanguage'||key==='voiceGender'?{voiceURI:''}:{})});if(key==='voiceStyle'||key==='voiceGender'){renderDialog();return}const output=dialog.querySelector(`[data-pref-output="${key}"]`);if(output&&typeof preferences[key]==='number')output.textContent=preferences[key].toFixed(2)+(key==='rate'?'×':'');if(key==='voiceLanguage')refreshVoices();status(describeSaved())})});
    dialog.querySelectorAll('[data-voice-preset]').forEach(button=>{button.onclick=()=>{const presets={careful:{rate:.8,pitch:1},natural:{rate:1,pitch:1},brisk:{rate:1.15,pitch:1}};update(presets[button.dataset.voicePreset]);renderDialog()}});
    dialog.querySelector('[data-voice-test]').onclick=()=>{
      stopVoice();const spoken=getNarrationLanguage(),speech=getSpeechOptions(spoken),voice=voices().find(v=>v.voiceURI===speech.voiceURI)||null,Utterance=environment.SpeechSynthesisUtterance;
      if(!voice || !synth?.speak || !Utterance){status(words('目前沒有相符語音；請先安裝系統語音。','No matching voice is available; install a system voice first.'));return}
      const samples={zh:'先確認目標，再觀察證據，最後完成這一道工程工序。',en:'First confirm the objective. Then inspect the evidence and complete this engineering step.',ja:'目標を確認してから、証拠を観察し、この工程を完了しましょう。',ko:'목표를 확인하고 증거를 살펴본 뒤 이 공정 단계를 완료하세요.',es:'Primero confirma el objetivo. Después revisa las pruebas y completa este paso.',fr:'Confirmez l’objectif, examinez les preuves, puis terminez cette étape.',de:'Prüfen Sie zuerst das Ziel, dann die Nachweise, und schließen Sie diesen Schritt ab.',pt:'Confirme o objetivo, examine as evidências e conclua esta etapa.',it:'Conferma l’obiettivo, osserva le prove e completa questa fase.'};
      const sample=samples[base(spoken)] || `${voice.name}. 1, 2, 3.`;
      const item=new Utterance(sample);speaking=item;item.lang=voice.lang;item.voice=voice;item.rate=speech.rate;item.pitch=speech.pitch;if(speech.genderApproximated)status(words('此裝置沒有相符性別的語音，已用音高近似；可在系統安裝更多語音。','No voice of that gender on this device; pitch is used as an approximation. Install more system voices for better results.'));
      item.onend=()=>{speaking=null;status(describeSaved())};item.onerror=()=>{speaking=null;status(words('語音未能播放；請試其他裝置語音。','Speech could not play; try another device voice.'))};
      try{synth.speak(item);status(words('正在試聽…','Playing preview…'))}catch{speaking=null;status(words('語音未能播放。','Speech could not play.'))}
    };
    dialog.querySelector('[data-voice-stop]').onclick=()=>{stopVoice();status(describeSaved())};
    dialog.querySelector('[data-preference-reset]').onclick=()=>{stopVoice();update({...DEFAULT_PREFERENCES});renderDialog()};
    dialog.querySelector('[data-preference-export]').onclick=()=>{const blob=new environment.Blob([JSON.stringify({format:'macgyver-workspace',version:1,preferences},null,2)],{type:'application/json'}),url=environment.URL.createObjectURL(blob),link=document.createElement('a');link.href=url;link.download='MacGyver_Workspace_Preferences.json';link.click();environment.setTimeout(()=>environment.URL.revokeObjectURL(url),1000);status(words('已匯出外觀與語音設定；未包含個資、帳號或學習進度。','Exported appearance and voice preferences without identity, account or learning progress data.'))};
    dialog.querySelector('[data-preference-import]').onchange=async event=>{const file=event.target.files?.[0];if(!file)return;try{if(file.size>12000)throw new Error('size');const data=JSON.parse(await file.text());if(data.format!=='macgyver-workspace'||data.version!==1||!data.preferences||typeof data.preferences!=='object'||Array.isArray(data.preferences))throw new Error('format');stopVoice();update(normalizePreferences(data.preferences));renderDialog();status(words('已匯入至目前學習檔案。','Imported into the current learning profile.'))}catch{status(words('無法匯入；請選擇本站匯出的設定 JSON（12 KB 以內）。','Import failed. Choose an exported workspace JSON file under 12 KB.'))}};
    refreshVoices();options.onRendered?.(dialog);
  };
  const open = () => {
    syncProfile();options.onOpen?.();opener=document?.activeElement;
    if(!dialog){dialog=document.createElement('dialog');dialog.className='preferences-dialog';dialog.id='preferencesDialog';dialog.setAttribute('aria-label',words('個人工作室設定','Personal workspace preferences'));document.body.appendChild(dialog);dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close()});dialog.addEventListener('close',()=>{stopVoice();opener?.focus?.()})}
    renderDialog();if(!dialog.open){if(dialog.showModal)dialog.showModal();else dialog.setAttribute('open','')}
  };
  media?.addEventListener?.('change',apply);synth?.addEventListener?.('voiceschanged',refreshVoices);
  const onStorage = event=>{if(event.key===preferenceKey(profileId)){try{preferences=normalizePreferences(JSON.parse(event.newValue||'null'));saved=true;apply();if(dialog?.open)renderDialog();notify()}catch{}}};
  environment.addEventListener?.('storage',onStorage);
  syncProfile();
  return {open,syncProfile,getNarrationLanguage,getSpeechOptions,update,get preferences(){return {...preferences}},destroy(){stopVoice();media?.removeEventListener?.('change',apply);synth?.removeEventListener?.('voiceschanged',refreshVoices);environment.removeEventListener?.('storage',onStorage);dialog?.remove()}};
}

export const SHOWCASES=Object.freeze([
  {id:'portrait',url:'https://kuonanhong.github.io/HoloArtisan_PortraitMuseum/',title:'肖像博物館',titleEn:'Portrait Museum',label:'HOLO ARTISAN / MUSEUM',icon:'◈',description:'探索 Holo Artisan 肖像博物館；在獨立展示頁感受藝術與互動的連結。',descriptionEn:'Explore the Holo Artisan Portrait Museum in its own interactive exhibition.'},
  {id:'technology',url:'https://kuonanhong.github.io/HoloArtisanDemo/',title:'技術展示區',titleEn:'Technology showcase',label:'HOLO ARTISAN / DEMO',icon:'⌘',description:'開啟 Holo Artisan 技術展示，延伸探索創作與工程應用。',descriptionEn:'Open the Holo Artisan demonstration to explore the connection between making and engineering.'}
]);
export function showcaseMarkup({zh=false}={}) {
  return `<section class="artisan-showcase" aria-labelledby="artisanShowcaseTitle"><div class="section-head"><div><span class="eyebrow">HOLO ARTISAN · ${zh?'創作者展示':'CREATOR SHOWCASE'}</span><h2 id="artisanShowcaseTitle">${zh?'藝術與工程，繼續探索':'Keep exploring art and engineering'}</h2><p class="subtext">${zh?'本站創作者的兩個獨立作品。由您選擇是否在此載入。':'Two independent projects by this site’s creator. Choose whether to load them here.'}</p></div></div><div class="showcase-tabs" role="tablist" aria-label="${zh?'Holo Artisan 展示':'Holo Artisan exhibits'}">${SHOWCASES.map((item,index)=>`<button type="button" class="showcase-tab" id="showcase-tab-${item.id}" role="tab" aria-selected="${!index}" aria-controls="showcase-panel-${item.id}" tabindex="${index?-1:0}" data-showcase-tab="${item.id}"><span aria-hidden="true">${item.icon}</span>${escape(zh?item.title:item.titleEn)}</button>`).join('')}</div>${SHOWCASES.map((item,index)=>`<div id="showcase-panel-${item.id}" class="showcase-panel" role="tabpanel" aria-labelledby="showcase-tab-${item.id}" ${index?'hidden':''} data-showcase-panel="${item.id}"><div class="showcase-description"><div><span class="eyebrow">${item.label}</span><h3>${escape(zh?item.title:item.titleEn)}</h3><p>${escape(zh?item.description:item.descriptionEn)}</p><small>${zh?'載入後連線 GitHub Pages；展示的功能及語言由原網站提供。':'Loading connects to GitHub Pages. Features and languages are provided by the original site.'}</small></div><div class="showcase-actions"><button type="button" class="button" data-showcase-load="${item.id}">${zh?'在此載入展示':'Load exhibit here'}</button><a class="button light" href="${item.url}" target="_blank" rel="noopener noreferrer">${zh?'獨立視窗開啟':'Open in new tab'} ↗</a><button type="button" class="text-link" data-showcase-unload="${item.id}" hidden>${zh?'關閉預覽':'Close preview'}</button></div></div><div data-showcase-frame="${item.id}" class="showcase-frame" hidden></div><p class="showcase-fallback" data-showcase-fallback="${item.id}" hidden>${zh?'若原網站限制內嵌、畫面空白或需要相機等裝置功能，請使用「獨立視窗開啟」。':'If embedding is blocked, the display is blank, or a device feature such as a camera is needed, use Open in new tab.'}</p></div>`).join('')}</section>`;
}
export function bindShowcase(root=globalThis.document,{onRendered}={}) {
  for(const section of root?.querySelectorAll?.('.artisan-showcase') || []){
    if(section.dataset.bound)continue;section.dataset.bound='true';
    const tabs=[...section.querySelectorAll('[data-showcase-tab]')];
    const activate = (id,focus=false) => {tabs.forEach(tab=>{const selected=tab.dataset.showcaseTab===id;tab.setAttribute('aria-selected',String(selected));tab.tabIndex=selected?0:-1;if(selected&&focus)tab.focus()});section.querySelectorAll('[data-showcase-panel]').forEach(panel=>{panel.hidden=panel.dataset.showcasePanel!==id;if(panel.hidden){panel.querySelectorAll('iframe').forEach(frame=>frame.remove());panel.querySelector('[data-showcase-frame]').hidden=true;panel.querySelector('[data-showcase-load]').hidden=false;panel.querySelector('[data-showcase-unload]').hidden=true;panel.querySelector('[data-showcase-fallback]').hidden=true}})};
    tabs.forEach((tab,index)=>{tab.onclick=()=>activate(tab.dataset.showcaseTab);tab.onkeydown=event=>{const direction=section.ownerDocument.documentElement.dir==='rtl'?-1:1;let next;if(event.key==='ArrowRight')next=(index+direction+tabs.length)%tabs.length;if(event.key==='ArrowLeft')next=(index-direction+tabs.length)%tabs.length;if(event.key==='Home')next=0;if(event.key==='End')next=tabs.length-1;if(next!==undefined){event.preventDefault();activate(tabs[next].dataset.showcaseTab,true)}}});
    section.querySelectorAll('[data-showcase-load]').forEach(button=>{button.onclick=()=>{const item=SHOWCASES.find(entry=>entry.id===button.dataset.showcaseLoad);if(!item)return;const slot=section.querySelector(`[data-showcase-frame="${item.id}"]`),frame=section.ownerDocument.createElement('iframe');frame.src=item.url;frame.title=item.titleEn;frame.loading='lazy';frame.referrerPolicy='strict-origin-when-cross-origin';frame.setAttribute('sandbox','allow-scripts allow-same-origin allow-forms allow-popups allow-popups-to-escape-sandbox allow-downloads allow-presentation');frame.setAttribute('allow','fullscreen');frame.setAttribute('allowfullscreen','');slot.replaceChildren(frame);slot.hidden=false;button.hidden=true;section.querySelector(`[data-showcase-unload="${item.id}"]`).hidden=false;section.querySelector(`[data-showcase-fallback="${item.id}"]`).hidden=false;onRendered?.(section)}});
    section.querySelectorAll('[data-showcase-unload]').forEach(button=>{button.onclick=()=>{const id=button.dataset.showcaseUnload,slot=section.querySelector(`[data-showcase-frame="${id}"]`);slot.replaceChildren();slot.hidden=true;button.hidden=true;section.querySelector(`[data-showcase-load="${id}"]`).hidden=false;section.querySelector(`[data-showcase-fallback="${id}"]`).hidden=true}});
  }
}
