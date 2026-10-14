/** User-started, speech-paced teaching. Importing this module has no DOM effects.
 * Speech availability is device dependent. Text mode always waits for Next.
 * References: MDN SpeechSynthesis voiceschanged / cancel and utterance error.
 */
import { sampleDemonstration } from './demo-controller.js';

const normalize = value => String(value || 'en').replaceAll('_', '-').toLowerCase();
const base = value => normalize(value).split('-')[0];
const core = value => ['en', 'zh'].includes(base(value));
const english = (object, field = 'title') => String(object?.[field + 'En'] || object?.[field] || '');
const field = (object, name, zh) => String(zh ? object?.[name] || object?.[name + 'En'] || '' : english(object, name));
const bilingual = (value, zh) => typeof value === 'string' ? value : String(value?.[zh ? 'zh' : 'en'] || value?.en || value?.zh || '');
const escape = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[char]));
let activeGuide = null;

/** Prefer an exact locale, then a voice for the same language; never another language. */
export function selectMentorVoice(voices, language, preferredURI = '') {
  const available = Array.from(voices || []).filter(voice => base(voice.lang) === base(language));
  return available.find(voice => preferredURI && voice.voiceURI === preferredURI) || available.find(voice => normalize(voice.lang) === normalize(language)) || available.find(voice => voice.default) || available[0] || null;
}

/** Bounded utterances avoid browser engines stalling on long paragraphs. */
export function splitMentorText(text, limit = 220) {
  const chars = Array.from(String(text || '').trim()), parts = [];
  while (chars.length) {
    let length = Math.min(limit, chars.length);
    if (length < chars.length) {
      for (let index = length - 1; index > limit * .45; index--) {
        if (/[。！？.!?;；\n\s]/u.test(chars[index])) { length = index + 1; break; }
      }
    }
    const part = chars.splice(0, length).join('').trim();
    if (part) parts.push(part);
  }
  return parts;
}

/** Public curriculum only. Deliberately excludes quiz answers and learner notes. */
export function buildMentorSegments({ course = {}, step = {}, spec = {}, frames = [], zh = false } = {}) {
  const lesson = [], tour = [], demo = [];
  const add = (list, id, text, target, extra = {}) => {
    if (text?.trim()) list.push({ id, phase: list === lesson ? 'lesson' : list === tour ? 'tour' : 'demo', text: text.trim(), language: zh ? 'zh-TW' : 'en', target, ...extra });
  };
  add(lesson, 'lesson-title', zh ? `這道工序是：${field(step,'title',zh)}。先理解目標與判斷依據，再看師傅示範，最後自己操作。` : `This operation is ${field(step,'title',zh)}. First understand its purpose and evidence, then watch the demonstration and practice.`, '#stepHeading');
  for (const [name, zhTitle, enTitle, target] of [
    ['objective','本工序目標','Objective','#lessonSection'],
    ['instruction','操作方法','Procedure','#lessonSection .instruction'],
    ['observation','觀察重點','What to observe','#lessonSection .observation'],
    ['failure','失敗判讀','Diagnosing a failure','#lessonSection .failure'],
  ]) {
    const text = field(step, name, zh);
    if (text) add(lesson, 'lesson-' + name, `${zh ? zhTitle : enTitle}: ${text}`, target);
  }
  (step.knowledge || []).forEach((point, index) => add(lesson, `lesson-knowledge-${index}`, `${field(point,'title',zh)}. ${field(point,'text',zh)}`, `#lessonSection .knowledge details:nth-of-type(${index + 1})`));
  if (field(step, 'check', zh)) add(lesson, 'lesson-check', `${zh ? '驗收條件' : 'Acceptance criteria'}: ${field(step,'check',zh)}`, '#quizSection');
  if (bilingual(spec.instruction, zh)) add(lesson, 'lesson-task', `${zh ? '本頁練習' : 'The on-screen exercise'}: ${bilingual(spec.instruction,zh)} ${zh ? '這是教學示意；實際設備須另依正式規範與合格人員作業。' : 'This is a teaching model. Real equipment requires its formal procedures and qualified personnel.'}`, '#exerciseTask');

  const control = (id, zhText, enText, target) => add(tour, 'tour-' + id, zh ? zhText : enText, target);
  control('keyboard', '點一下啟用鍵盤，再使用工作台快捷鍵。文字輸入欄位不控制工具；Esc 可離開鍵盤操作。手機和平板可使用畫面按鈕。', 'Enable the workshop keyboard before using shortcuts. Typing fields do not move the tool; Escape leaves keyboard control. On phones and tablets, use the on-screen buttons.', '#activateKeyboard');
  control('grab', '先按抓取，再移動工具。空白鍵可切換抓取與放開；焦點在按鈕時，空白鍵操作該按鈕。操作完記得放開。', 'Grab the tool before moving it. Space toggles grab and release unless a button has focus, where Space activates that button. Release when the operation is finished.', '#grab');
  for (const [id, key, zhText, enText] of [
    ['y-','↑ / W','沿 Y 軸負方向移動','Move in the negative Y direction'],
    ['x-','← / A','沿 X 軸負方向移動','Move in the negative X direction'],
    ['y+','↓ / S','沿 Y 軸正方向移動','Move in the positive Y direction'],
    ['x+','→ / D','沿 X 軸正方向移動','Move in the positive X direction'],
    ['z+','I / PageUp','抬高工具，沿 Z 軸正方向移動','Raise the tool in the positive Z direction'],
    ['z-','K / PageDown','降低工具，沿 Z 軸負方向移動','Lower the tool in the negative Z direction'],
    ['r-','J / Q','向左旋轉工具','Rotate the tool to the left'],
    ['r+','L / E','向右旋轉工具','Rotate the tool to the right'],
  ]) {
    const arrows={'y-':['上方向鍵','Up arrow'],'x-':['左方向鍵','Left arrow'],'y+':['下方向鍵','Down arrow'],'x+':['右方向鍵','Right arrow']};
    control(id, `${arrows[id] ? arrows[id][0] + '或 ' : ''}${key} 鍵，或按住這個按鈕：${zhText}。放開便停止移動。`, `${arrows[id] ? arrows[id][1] + ', ' : ''}${key}, or hold this button: ${enText}. Release to stop.`, `[data-motion="${id}"]`);
  }
  control('precision', '精細模式降低每次移動幅度。對位接近目標時使用；鍵盤也可按住 Shift 暫時精細移動。', 'Precision mode reduces each movement. Use it near the target; holding Shift also provides fine movement.', '#precision');
  control('snap', '吸附協助最後對位。先檢查工具與目標的位置、方向；吸附不會替你完成本工序的判讀或驗收。', 'Snap assists final alignment. Check the tool position and orientation first. Snapping does not complete the task decision or acceptance check.', '#snap');
  control('undo', '復原會還原前一次保存的工具姿態、任務設定與練習紀錄，方便比較與修正。鍵盤可用 Ctrl 或 Command 加 Z。', 'Undo restores the previously saved tool pose, task settings and practice record so you can compare and correct them. The shortcut is Control or Command plus Z.', '#undo');
  control('reset', '重設將工具回到起始姿態。需要重新練習抓取、移動、放開時可使用。', 'Reset returns the tool to its starting pose. Use it to practice grabbing, moving and releasing again.', '#resetPose');
  control('assist', '組合輔助會逐步帶動學徒工具、調整任務控制、記錄判讀並放開工具；可暫停或重播。請觀察每個動作，最後親自確認操作證據並回答驗收題。', 'Assembly assist moves the apprentice tool, adjusts the task controls, records the decision and releases the tool in sequence. You can pause or replay it. Observe each action, then confirm the operation evidence and answer the acceptance question yourself.', '#assist');
  for (const item of spec.controls || []) control('value-' + item.id, `這個滑桿控制${bilingual(item.label,true)}${item.unit ? `，顯示單位是 ${item.unit}` : ''}。一次改一個量，對照讀值與師傅結果；這些是示意參數，不是生產配方。`, `This slider controls ${bilingual(item.label,false)}${item.unit ? `, displayed in ${item.unit}` : ''}. Change one quantity at a time and compare the readout with the mentor. These are teaching parameters, not a production recipe.`, `[data-exercise-control="${item.id}"]`);
  if (spec.controls?.length) control('record', '讀值不需要改變時，也請按確認目前讀值，表示你已檢查所有控制量。', 'When a value already looks correct, confirm the current readings to record that you inspected each control.', '#confirmReadings');
  if (spec.choices?.length) control('choice', '比較這裡的判讀選項，依觀察證據選擇。示範會說明師傅的判斷；練習時請自己選擇。', 'Compare these decisions and select one using the observed evidence. The demonstration shows the mentor’s decision; choose for yourself during practice.', '.exercise-choices');
  if (spec.mode === 'inspect') control('observe', '完成判讀後記錄觀察，再檢查證據區是否符合驗收條件。', 'Record the observation after making the decision, then check whether the evidence meets the acceptance criteria.', '#observeExercise');
  if (spec.mode === 'process') control('perform', '先核對參數和判讀，再執行示意製程。改變參數之後，需要重新執行並檢查結果。', 'Check the parameters and decision before running the teaching process. After changing a parameter, run it again and inspect the result.', '#performExercise');
  control('submit', '完成自己的移動、任務操作並放開工具後，按這裡保存操作證據；接著回答知識驗收題。略過按鍵導覽不等於完成工序。', 'After moving the tool, completing the task and releasing it, save the operation evidence here and answer the knowledge check. Skipping this control tour does not complete the operation.', '#place');

  frames.forEach((frame, index) => {
    let target = ({identify:'#mentorModel',grab:'#grab',lift:'[data-motion="z+"]',move:'#handControls',position:'[data-motion="z-"]',choose:'.exercise-choices',observe:'#observeExercise',perform:'#performExercise',release:'#grab',ready:'#learnerModel'})[frame.action] || '#mentorModel';
    if (frame.action === 'adjust') {
      const previous = frames[index - 1]?.state.exercise.values || {};
      const changed = (spec.controls || []).find(item => frame.state.exercise.values[item.id] !== previous[item.id]);
      const named = (spec.controls || []).find(item => bilingual(frame.label,zh).startsWith(bilingual(item.label,zh)));
      if (changed || named) target = `[data-exercise-control="${(changed || named).id}"]`;
    }
    add(demo, `demo-${index}`, bilingual(frame.label,zh), target, {frameIndex:index});
  });
  return { lesson, tour, demo };
}

/** Optional authenticated translation of public teaching text. Nothing is rehosted. */
export async function translateMentorSegments({ segments, language, signal, fetchImpl = globalThis.fetch } = {}) {
  if (typeof fetchImpl !== 'function') throw new Error('Translation unavailable');
  const pieces = (segments || []).flatMap(segment => splitMentorText(segment.text, 1800).map(text => ({id:segment.id,text})));
  const translated = new Map();
  for (let offset = 0; offset < pieces.length;) {
    if (signal?.aborted) throw new Error('Translation cancelled');
    const batch = []; let length = 0;
    while (offset < pieces.length && batch.length < 12 && length + pieces[offset].text.length <= 4000) { const part = pieces[offset++]; batch.push(part); length += part.text.length; }
    const response = await fetchImpl('/api/translate', {method:'POST',credentials:'same-origin',headers:{'Content-Type':'application/json',Accept:'application/json'},body:JSON.stringify({language,texts:batch.map(item=>item.text)}),signal});
    if (!response.ok) throw new Error('Narration translation unavailable');
    const result = await response.json();
    if (!Array.isArray(result.translations) || result.translations.length !== batch.length || result.translations.some(text => typeof text !== 'string' || !text.trim() || text.length > 12000)) throw new Error('Incomplete narration translation');
    result.translations.forEach((text,index) => translated.set(batch[index].id, [...(translated.get(batch[index].id) || []), text.trim()]));
  }
  return {language,segments:(segments || []).map(segment => ({id:segment.id,text:(translated.get(segment.id) || []).join(' ')}))};
}

export function mentorGuideMarkup({ zh = false } = {}) {
  const text = zh ? ['師傅逐段講解','按「開始示範」聽完整工序。語音依裝置支援；無語音時按下一段閱讀。','下一段','重看按鍵導覽','略過按鍵導覽','停止講解'] : ['Mentor, one section at a time','Start the demonstration to hear the full procedure. Voice availability depends on this device; use Next section to read without audio.','Next section','Review controls','Skip controls tour','Stop narration'];
  return `<section class="mentor-guide" data-no-translate aria-label="${escape(text[0])}"><p id="mentorGuideStatus" role="status">${escape(text[0])}</p><p id="mentorGuideText" aria-live="polite" aria-atomic="true">${escape(text[1])}</p><div class="mentor-guide-actions"><button id="mentorGuideNext" class="button light" type="button" disabled>${escape(text[2])}</button><button id="mentorGuideTour" class="button light" type="button">${escape(text[3])}</button><button id="mentorGuideSkipTour" class="button light" type="button" disabled>${escape(text[4])}</button><button id="mentorGuideStop" class="button light" type="button" disabled>${escape(text[5])}</button></div></section>`;
}

/** All effects begin here, never at module import. onFrame only changes mentor art.
 * translate returns {language,segments:[{id,text}]} for the exact requested locale.
 * onComplete({kind}) reports 'procedure', 'lesson', or 'tour'; only procedure
 * completion may satisfy the app's demonstration gate. No learner state is edited.
 */
export function createMentorGuide(options = {}) {
  const root = options.root ?? globalThis.document;
  const document = root?.ownerDocument || root;
  const environment = options.environment || document?.defaultView || globalThis;
  const synth = options.speechSynthesis ?? environment.speechSynthesis;
  const Utterance = options.Utterance ?? environment.SpeechSynthesisUtterance;
  const schedule = options.schedule || ((fn,ms) => setTimeout(fn,ms));
  const cancelTimer = options.cancel || clearTimeout;
  const now = options.now || (() => Date.now());
  const frames = options.frames || [];
  const reducedMotion = options.reducedMotion ?? !!environment.matchMedia?.('(prefers-reduced-motion: reduce)').matches;
  let language = options.language || (options.zh ? 'zh-TW' : 'en'), zh = options.zh ?? base(language) === 'zh';
  let status = 'idle', phase = '', kind = '', queue = [], index = -1, generation = 0, disposed = false, voiceEnabled = true, tourSkipped = false;
  let utterance = null, activeTimer = null, animationTimer = null, waitCleanup = null, translationController = null, translationTimer = null;
  let pointer = null, target = null, currentFrame = null, fallbackReason = '', selectedVoice = null;
  const listeners = [], query = selector => {try{return root?.querySelector?.(selector) || null}catch{return null}};
  const listen = (element,event,handler,opts) => {if(!element?.addEventListener)return;element.addEventListener(event,handler,opts);listeners.push(()=>element.removeEventListener(event,handler,opts))};
  const labels = () => zh ? {idle:'先點擊開始示範',preparing:'準備本語言講解…',speaking:'師傅講解中',waiting:'文字模式：讀完後按下一段',paused:'講解已暫停；按播放繼續',complete:'本段導覽已完成',stopped:'講解已停止',lesson:'工序說明',tour:'按鍵導覽',demo:'師傅示範',unavailable:'此裝置沒有可用的相符語音',translation:'本語言翻譯尚未可用；以下保留英文原文',error:'語音無法播放，已切換文字',timeout:'語音回應逾時，已切換文字'} : {idle:'Click to start the demonstration',preparing:'Preparing narration in this language…',speaking:'Mentor is speaking',waiting:'Text mode: read, then choose Next section',paused:'Narration paused; press play to continue',complete:'This guide is complete',stopped:'Narration stopped',lesson:'Procedure',tour:'Controls tour',demo:'Demonstration',unavailable:'No matching voice is available on this device',translation:'Translation is unavailable; the English source text remains below',error:'Speech could not play; switched to text',timeout:'Speech timed out; switched to text'};
  const updateStatus = (next = status, reason = '') => {
    status = next;
    const words = labels(), label = `${words[status] || status}${phase ? ` · ${words[phase] || phase} ${Math.max(index+1,0)}/${queue.length}` : ''}${reason ? ` · ${words[reason] || reason}` : ''}`;
    const node = query('#mentorGuideStatus'); if (node) node.textContent = label;
    const nextButton=query('#mentorGuideNext');if(nextButton)nextButton.disabled=!['speaking','waiting','paused'].includes(status);
    const stopButton=query('#mentorGuideStop');if(stopButton)stopButton.disabled=['idle','stopped','complete'].includes(status);
    const tourButton=query('#mentorGuideTour');if(tourButton)tourButton.disabled=kind==='procedure'&&['preparing','speaking','waiting','paused'].includes(status);
    const skipButton=query('#mentorGuideSkipTour');if(skipButton)skipButton.disabled=tourSkipped||!queue.slice(Math.max(0,index)).some(segment=>segment.phase==='tour')||['idle','stopped','complete'].includes(status);
    options.onStatus?.({status,phase,kind,index,total:queue.length,language,textLanguage:queue[index]?.language || '',reason,label,tourSkipped});
  };
  const clearSpeaking = () => {
    if (activeTimer !== null) {cancelTimer(activeTimer);activeTimer=null}
    if (animationTimer !== null) {cancelTimer(animationTimer);animationTimer=null}
    if (utterance) {utterance.onend=null;utterance.onerror=null;utterance.onstart=null;utterance=null;try{synth?.cancel()}catch{}}
    if(waitCleanup){waitCleanup();waitCleanup=null}
  };
  const abortTranslation = () => {translationController?.abort();translationController=null;if(translationTimer!==null){cancelTimer(translationTimer);translationTimer=null}};
  const hidePointer = () => {target?.classList?.remove('mentor-guide-target');target=null;if(pointer)pointer.hidden=true};
  const visibleViewport = () => {
    const width=environment.innerWidth||1024,height=environment.innerHeight||768;
    const dock=query('.workshop-action-dock'),rect=dock?.getBoundingClientRect?.();
    // The dock may be in normal flow in a host; reserve space only when it
    // actually occupies the bottom of this viewport.
    const bottom=rect&&rect.top>0&&rect.top<height&&rect.bottom>=height-4?Math.max(96,rect.top-16):height;
    return {width,height,bottom};
  };
  const positionPointer = () => {
    if(!target?.isConnected || !pointer)return;
    const rect=target.getBoundingClientRect(),{width,bottom}=visibleViewport();
    if(rect.bottom<0||rect.top>bottom||rect.right<0||rect.left>width){pointer.hidden=true;return}
    pointer.hidden=false;
    const x=Math.max(22,Math.min(width-22,rect.left+rect.width/2));
    const above=rect.top>=58,y=Math.max(22,Math.min(bottom-22,above?rect.top-38:rect.bottom+38));
    pointer.style.left=`${x}px`;pointer.style.top=`${y}px`;pointer.style.transform=`translate(-50%, -50%) rotate(${above?90:-90}deg)`;
  };
  const pointTo = selector => {
    hidePointer();target=query(selector);if(!target)return;
    if(target.tagName==='DETAILS')target.open=true;
    for(let detail=target.closest?.('details');detail;detail=detail.parentElement?.closest?.('details'))detail.open=true;
    target.classList?.add('mentor-guide-target');
    const {bottom}=visibleViewport(),height=target.getBoundingClientRect?.().height||0,tall=height>Math.max(120,(bottom-64)*.65);
    target.scrollIntoView?.({block:tall?'start':'center',inline:'nearest',behavior:'auto'});
    // Center a button/slider in usable space, not beneath the fixed Next dock.
    // Tall lesson sections retain their heading and first paragraph in view.
    const rect=target.getBoundingClientRect?.();
    if(rect&&environment.scrollBy){const shift=tall?rect.top-64:rect.top+height/2-(64+bottom)/2;if(Math.abs(shift)>1)environment.scrollBy({top:shift,left:0,behavior:'auto'})}
    if(!pointer&&document?.createElement){pointer=document.createElement('span');pointer.className='mentor-guide-arrow';pointer.textContent='➜';pointer.setAttribute('aria-hidden','true');pointer.setAttribute('data-no-translate','');Object.assign(pointer.style,{position:'fixed',pointerEvents:'none'});document.body?.appendChild(pointer)}
    positionPointer();
  };
  const valid = token => !disposed && token === generation;
  const speechPreferences = () => {
    let settings={};try{settings=options.getSpeechOptions?.(language) || options.speechOptions || {}}catch{}
    const bounded=(value,fallback)=>typeof value==='number'&&Number.isFinite(value)?Math.max(.6,Math.min(1.4,value)):fallback;
    return {voiceURI:typeof settings.voiceURI==='string'?settings.voiceURI:'',rate:bounded(settings.rate,.9),pitch:bounded(settings.pitch,1)};
  };
  const emitFrame = (frameIndex,token) => {
    if(!frames[frameIndex])return;
    const at=frames[frameIndex].at,previous=frames[Math.max(0,frameIndex-1)].at,start=now(),duration=reducedMotion?0:Math.min(500,Math.max(0,at-previous));
    const emit = () => {
      if(!valid(token))return;
      const amount=duration?Math.min(1,(now()-start)/duration):1;
      const sampled=sampleDemonstration(frames,previous+(at-previous)*amount,reducedMotion);
      currentFrame={...sampled,index:frameIndex,action:frames[frameIndex].action,label:frames[frameIndex].label};
      options.onFrame?.(currentFrame);
      if(amount<1)animationTimer=schedule(emit,40);else animationTimer=null;
    };emit();
  };
  const finish = () => {clearSpeaking();hidePointer();phase='';updateStatus('complete');if(activeGuide===api)activeGuide=null;options.onComplete?.({kind,language,tourSkipped})};
  const settleFrame = () => {
    const frameIndex=queue[index]?.frameIndex;
    if(frameIndex===undefined||!frames[frameIndex])return;
    if(animationTimer!==null){cancelTimer(animationTimer);animationTimer=null}
    currentFrame=sampleDemonstration(frames,frames[frameIndex].at,true);options.onFrame?.(currentFrame);
  };
  const fallback = reason => {voiceEnabled=false;fallbackReason=reason;clearSpeaking();settleFrame();updateStatus('waiting',reason)};
  const awaitVoice = token => {
    let voices=[];try{voices=synth.getVoices()||[]}catch{}
    const match=selectMentorVoice(voices,language,speechPreferences().voiceURI);if(match)return Promise.resolve(match);
    return new Promise(resolve => {
      let settled=false,timer=null;
      const end=value=>{if(settled)return;settled=true;if(timer!==null)cancelTimer(timer);synth.removeEventListener?.('voiceschanged',changed);waitCleanup=null;resolve(value)};
      const changed=()=>{if(!valid(token)){end(null);return}let list=[];try{list=synth.getVoices()||[]}catch{}const voice=selectMentorVoice(list,language,speechPreferences().voiceURI);if(voice)end(voice)};
      synth.addEventListener?.('voiceschanged',changed);
      timer=schedule(()=>end(null),options.voiceWaitMs??1800);
      waitCleanup=()=>end(null);
      changed();
    });
  };
  const speakCurrent = async token => {
    if(!voiceEnabled){settleFrame();updateStatus('waiting',fallbackReason);return}
    const segment=queue[index];
    if(!synth?.speak||!Utterance){fallback('unavailable');return}
    if(base(segment.language)!==base(language)){fallback('translation');return}
    updateStatus('preparing');
    // Re-read preferences between sections. Do not retain a previously selected
    // voice after the member changes it, and never use a different language.
    selectedVoice=await awaitVoice(token);
    if(!valid(token))return;
    if(!selectedVoice){fallback('unavailable');return}
    const chunks=splitMentorText(segment.text);let chunk=0;
    const speakPart = () => {
      if(!valid(token))return;
      const item=new Utterance(chunks[chunk]),settings=speechPreferences();utterance=item;item.voice=selectedVoice;item.lang=selectedVoice.lang||language;item.rate=settings.rate;item.pitch=settings.pitch;item.volume=1;
      const timeout=()=>{if(valid(token))fallback('timeout')};
      activeTimer=schedule(timeout,options.startTimeoutMs??8000);
      item.onstart=()=>{if(!valid(token))return;if(activeTimer!==null)cancelTimer(activeTimer);activeTimer=schedule(timeout,options.utteranceTimeoutMs??Math.min(60000,Math.max(15000,chunks[chunk].length*180)));updateStatus('speaking')};
      item.onerror=()=>{if(valid(token))fallback('error')};
      item.onend=()=>{if(!valid(token))return;if(activeTimer!==null)cancelTimer(activeTimer);activeTimer=null;item.onend=null;item.onerror=null;item.onstart=null;utterance=null;chunk++;if(chunk<chunks.length)speakPart();else advance()};
      try{updateStatus('speaking');synth.speak(item)}catch{fallback('error')}
    };speakPart();
  };
  const showCurrent = () => {
    if(disposed)return;
    const token=++generation;clearSpeaking();
    if(index>=queue.length){finish();return}
    const segment=queue[index];phase=segment.phase;
    const node=query('#mentorGuideText');if(node){node.textContent=segment.text;node.lang=segment.language;node.dir=['ar','he','fa','ur'].includes(base(segment.language))?'rtl':'auto'}
    pointTo(segment.target);if(segment.frameIndex!==undefined)emitFrame(segment.frameIndex,token);
    options.onText?.({...segment,index,total:queue.length});
    void speakCurrent(token);
  };
  const advance = () => {index++;while(tourSkipped&&queue[index]?.phase==='tour')index++;showCurrent()};
  const start = async (mode,{includeTour=true,voice=true}={}) => {
    if(disposed)return;
    api.stop('restart');if(activeGuide&&activeGuide!==api)activeGuide.stop('superseded');activeGuide=api;
    kind=mode;phase='';voiceEnabled=voice;fallbackReason='';tourSkipped=!includeTour;selectedVoice=null;
    const built=buildMentorSegments({...options,zh:core(language)?base(language)==='zh':false});
    queue=mode==='lesson'?built.lesson:mode==='tour'?built.tour:[...built.lesson,...(includeTour?built.tour:[]),...built.demo];
    index=0;const token=++generation;
    if(!core(language)){
      updateStatus('preparing');
      if(typeof options.translate==='function'){
        translationController=new AbortController();
        let rejectTimeout;
        const timeout=new Promise((_,reject)=>{rejectTimeout=reject;translationTimer=schedule(()=>{translationController?.abort();reject(new Error('Translation timed out'))},options.translationTimeoutMs??45000)});
        try{
          const result=await Promise.race([options.translate({segments:queue.map(({id,text})=>({id,text})),language,signal:translationController.signal}),timeout]);
          if(!valid(token))return;
          if(normalize(result?.language)!==normalize(language)||!Array.isArray(result.segments)||result.segments.length!==queue.length)throw new Error('Translation language or length mismatch');
          const byId=new Map(result.segments.map(segment=>[segment.id,segment.text]));
          if(byId.size!==queue.length||queue.some(segment=>typeof byId.get(segment.id)!=='string'||!byId.get(segment.id).trim()))throw new Error('Incomplete translated narration');
          queue=queue.map(segment=>({...segment,text:byId.get(segment.id).trim(),language}));
        }catch{if(!valid(token))return;voiceEnabled=false;fallbackReason='translation'}
        finally{if(valid(token)){abortTranslation();rejectTimeout=null}}
      }else{voiceEnabled=false;fallbackReason='translation'}
    }
    if(valid(token))showCurrent();
  };
  const api={
    get status(){return status},get phase(){return phase},get frame(){return currentFrame},get index(){return index},get kind(){return kind},
    begin:settings=>start('procedure',settings),readLesson:settings=>start('lesson',settings),startTour:settings=>start('tour',settings),
    next(){if(disposed||!['speaking','waiting','paused'].includes(status))return;advance()},
    skipTour(){if(disposed)return;tourSkipped=true;if(phase==='tour'){while(queue[index]?.phase==='tour')index++;showCurrent()}else updateStatus(status,fallbackReason)},
    pause(){if(disposed||!['speaking','waiting','preparing'].includes(status))return;++generation;clearSpeaking();abortTranslation();hidePointer();updateStatus('paused')},
    resume(){if(disposed||status!=='paused')return;if(!queue.length)return;showCurrent()},
    stop(reason='stopped'){if(disposed)return;++generation;clearSpeaking();abortTranslation();hidePointer();phase='';updateStatus('stopped',reason==='restart'?'':reason);if(activeGuide===api)activeGuide=null},
    setLanguage(value,isChinese=base(value)==='zh'){if(normalize(value)===normalize(language))return;api.stop('languagechange');language=value;zh=isChinese;selectedVoice=null;queue=[];index=-1;updateStatus('idle')},
    dispose(){if(disposed)return;api.stop();disposed=true;listeners.splice(0).forEach(remove=>remove());pointer?.remove();pointer=null;status='disposed'},
  };
  for(const [selector,action] of [['#mentorGuideNext',()=>api.next()],['#mentorGuideTour',()=>api.startTour()],['#mentorGuideSkipTour',()=>api.skipTour()],['#mentorGuideStop',()=>api.stop()]])listen(query(selector),'click',action);
  for(const event of ['hashchange','popstate','pagehide'])listen(environment,event,()=>api.stop(event));
  listen(environment,'blur',()=>api.pause());listen(document,'visibilitychange',()=>{if(document.hidden)api.pause()});
  listen(environment,'languagechange',()=>api.stop('languagechange'));
  listen(environment,'scroll',positionPointer,true);listen(environment,'resize',positionPointer);
  updateStatus('idle');return api;
}
