/* V12 course access policy: the first stage ("第一節") of every guided course is
 * free; every other stage needs an active learning pass.
 *
 * Where the decision is enforced:
 *  - Python protected server (billing.protected): the server strips paid stages.
 *  - Supabase cloud: paid stage content can be removed from the public export
 *    and served from table course_content, readable only with an entitlement.
 *  - Plain static hosting without either: the lock is a UI policy only. The
 *    public JSON remains downloadable, so the owner must enable the protected
 *    export (see docs/PAYMENTS_V12_ZH.md) before selling real access.
 *  - The owner's offline package (file://) shows everything as a preview.
 */
const esc = v => String(v ?? '').replace(/[&<>"']/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;'}[c]));
let settings = {enabled: true, freeStagesPerCourse: 1, ownerPreviewOnFile: true};
let state = {mode: 'local', active: false, owner: false, expiresAt: null, planId: '', checked: false, error: ''};
let deps = {billing: () => ({}), cloud: () => null};
const contentCache = new Map(), hydratedCourses = new Map();
let contentEpoch=0,accessEpoch=0;
/** Called before any account switch: restore public stubs and discard private data. */
export function resetProtectedContent(){
  contentEpoch++;accessEpoch++;contentCache.clear();
  for(const [course,stages]of hydratedCourses)course.stages=stages;
  hydratedCourses.clear();
  state={mode:modeNow(),active:false,owner:false,expiresAt:null,planId:'',checked:false,error:''};
}

export function configurePaywall({config = globalThis.MG_CONFIG || {}, freeStages = 1, billing, cloud} = {}) {
  const c = config.paywall || {};
  settings = {
    enabled: c.enabled !== false,
    freeStagesPerCourse: Number.isInteger(c.freeStagesPerCourse) && c.freeStagesPerCourse >= 0 ? c.freeStagesPerCourse : freeStages,
    ownerPreviewOnFile: c.ownerPreviewOnFile !== false
  };
  if (billing) deps.billing = billing;
  if (cloud) deps.cloud = cloud;
  state.mode = modeNow();
  return {...settings};
}
function modeNow() {
  if (!settings.enabled) return 'disabled';
  if (globalThis.location?.protocol === 'file:' && settings.ownerPreviewOnFile) return 'owner-preview';
  if (deps.billing()?.protected) return 'server';
  if (deps.cloud()?.configured) return 'cloud';
  return 'local';
}
export function accessState() { return {...state, mode: modeNow(), freeStages: settings.freeStagesPerCourse}; }
export function freeStageCount() { return settings.freeStagesPerCourse; }
export function hasFullAccess() {
  const mode = modeNow();
  return mode === 'disabled' || mode === 'owner-preview' || state.active === true;
}
export function stageIsFree(stageIndex) { return Number(stageIndex) < settings.freeStagesPerCourse; }
/** step must come from allSteps() (it carries stageIndex). */
export function stepLocked(course, step) {
  if (!course || !step) return false;
  if (step.locked === true && !hasFullAccess()) return true;
  if (hasFullAccess()) return step.locked === true && !step.instruction && !step.objective;
  return !stageIsFree(step.stageIndex ?? 0);
}
export function firstLockedIndex(course, steps) { return steps.findIndex(s => stepLocked(course, s)); }

/** Refresh entitlement. Never throws; failures keep the course locked. */
export async function refreshAccess({user = null} = {}) {
  const generation=++accessEpoch,epoch=contentEpoch,mode=modeNow();
  const next={mode,active:false,owner:false,expiresAt:null,planId:'',checked:true,error:''};
  try {
    if(mode==='server'){
      // Only the authenticated server response grants owner/member access.
      if(user&&globalThis.fetch){const r=await fetch('/api/billing/me',{credentials:'same-origin',cache:'no-store'});if(r.ok){const data=await r.json(),now=Date.now()/1000;const live=(data.entitlements||[]).filter(e=>!e.revokedAt&&Number(e.expiresAt)>now&&Number(e.startsAt||0)<=now&&e.mode===(deps.billing()?.mode));next.owner=data.owner===true&&data.active===true;next.active=next.owner||live.length>0;next.planId=next.owner?'owner':'';next.expiresAt=next.owner?null:live.length?Math.max(...live.map(e=>Number(e.expiresAt)))*1000:null;}}
    }else if(mode==='cloud'&&user&&deps.cloud()?.myAccess){const access=await deps.cloud().myAccess();next.active=access?.active===true;next.expiresAt=access?.expiresAt?Date.parse(access.expiresAt)||null:null;next.planId=access?.planId||'';}
  }catch(error){next.active=false;next.error=String(error?.message||error);}
  if(generation===accessEpoch&&epoch===contentEpoch)state=next;
  return accessState();
}

/** Replace stub stages with protected content from Supabase when entitled. */
export async function hydrateProtectedStages(course) {
  const cloud=deps.cloud(),epoch=contentEpoch;
  if(!course?.stages||modeNow()!=='cloud'||!state.active||!cloud?.loadCourseContent)return course;
  if(!course.stages.some((stage,i)=>!stageIsFree(i)&&stage.steps?.some(s=>s.locked===true)))return course;
  const key=course.id;
  if(!contentCache.has(key)){
    const pending=Promise.resolve().then(()=>cloud.loadCourseContent(key)).catch(error=>{if(contentCache.get(key)===pending)contentCache.delete(key);throw error;});contentCache.set(key,pending);
  }
  const rows=await contentCache.get(key);
  if(epoch!==contentEpoch||cloud!==deps.cloud()||modeNow()!=='cloud'||!state.active)return course;
  const byIndex=new Map((rows||[]).map(row=>[Number(row.stage_index),row.payload]));
  const stages=course.stages.map((stage,i)=>{if(stageIsFree(i))return stage;const full=byIndex.get(i);if(!full||full.id!==stage.id||!Array.isArray(full.steps))return stage;return full.steps.map(s=>s.id).join('|')===stage.steps.map(s=>s.id).join('|')?full:stage;});
  if(stages.some((stage,i)=>!stageIsFree(i)&&stage.steps.some(step=>step.locked===true&&!step.instruction&&!step.objective))){contentCache.delete(key);throw Error('Member course content is incomplete. Retry after the course has been published.');}
  if(!hydratedCourses.has(course))hydratedCourses.set(course,course.stages);
  course.stages=stages;
  return course;
}

export function stageBadge(stageIndex, {zh = true} = {}) {
  if (modeNow() === 'disabled') return '';
  if (stageIsFree(stageIndex)) return `<span class="pay-badge free">${zh ? '免費試學' : 'Free'}</span>`;
  return hasFullAccess() ? `<span class="pay-badge open">${zh ? '已解鎖' : 'Unlocked'}</span>` : `<span class="pay-badge locked">🔒 ${zh ? '會員' : 'Members'}</span>`;
}

export function courseAccessSummary(course, {zh = true, priceText = ''} = {}) {
  const mode = modeNow(), pick = (a, b) => zh ? a : b;
  if (!course?.stages || mode === 'disabled') return '';
  const total = course.stages.reduce((n, st) => n + (st.steps?.length || 0), 0);
  const free = course.stages.slice(0, settings.freeStagesPerCourse).reduce((n, st) => n + (st.steps?.length || 0), 0);
  const paid = Math.max(0, total - free);
  let status;
  if (mode === 'owner-preview') status = pick('擁有者離線預覽：此版本可看全部內容；正式網站只開放第一節免費。', 'Owner offline preview: everything is visible here; the public site keeps only the first section free.');
  else if (state.owner && state.active) status = pick('管理員權限：全部免費與會員課程皆已開放，無需付款。', 'Site owner access: all free and member lessons are available without payment.');
  else if (state.active) status = pick('你的學習通行證有效，可學習全部階段。', 'Your learning pass is active; every stage is unlocked.') + (state.expiresAt ? ` ${pick('到期：', 'Expires: ')}${new Date(state.expiresAt).toLocaleDateString(zh ? 'zh-TW' : undefined)}` : '');
  let price = '';
  if (mode !== 'owner-preview' && !state.active) {
    status = pick(`第一節（${free} 步）免費試學；其餘 ${paid} 步需學習通行證。`, `The first section (${free} steps) is free; the other ${paid} steps need a learning pass.`);
    // V13: the local-currency price sits in its own untranslated span so every
    // language dictionary can translate the sentence regardless of currency.
    if (priceText) price = ` <span>${pick('學習通行證', 'Learning passes from')}</span> <span data-no-translate>${esc(priceText)}</span>${zh ? ' <span>起</span>' : ''}`;
  }
  return `<div class="course-access paywall-summary ${state.active || mode === 'owner-preview' ? '' : 'locked'}"><span>${pick('第一節免費 · 其餘會員', 'FIRST SECTION FREE · MEMBERS')}</span><p><span>${esc(status)}</span>${price}</p>${state.active || mode === 'owner-preview' ? '' : `<a class="button light" href="#membership">${pick('查看會員方案', 'View membership plans')} ↗</a>`}</div>`;
}

export function lockedStepMarkup(course, step, {zh = true, priceText = '', signedIn = false, firstFreeIndex = 0} = {}) {
  const pick = (a, b) => zh ? a : b, mode = modeNow();
  const title = zh ? (step.title || step.titleEn) : (step.titleEn || step.title);
  const stage = zh ? (step.stage?.title || step.stage?.titleEn) : (step.stage?.titleEn || step.stage?.title);
  const unlockNote = mode === 'local'
    ? pick('此網站尚未由站長啟用線上付款；啟用後即可購買通行證解鎖。', 'Online payment has not been enabled by the site owner yet; once it is, a pass unlocks this content.')
    : pick('購買學習通行證後，所有逐步課程的全部階段都會解鎖，並保存你的學習紀錄。', 'A learning pass unlocks every stage of every guided course and keeps your learning records.');
  return `<section class="task-card paywall-step" id="paywallStep"><span class="task-label">🔒 ${pick('會員內容', 'MEMBERS ONLY')} · ${esc(stage || '')}</span><h2>${esc(title || '')}</h2><p>${pick('本課第一節為免費試學，從這一節起需要有效的學習通行證。', 'The first section of this course is free; from this section on, an active learning pass is required.')}</p><ul class="paywall-includes"><li>${pick('全部 ', 'All ')}${course.stepCount || ''} ${pick('步逐步任務、知識點與驗收', 'guided tasks, knowledge points and checks')}</li><li>${pick('師傅示範、互動工作台與 AI 師傅', 'Mentor demonstrations, interactive workbench and AI mentor')}</li><li>${pick('跨裝置學習紀錄與平台完成證書', 'Cross-device records and platform completion certificates')}</li></ul><p class="subtext">${esc(unlockNote)}</p>${priceText ? `<p class="paywall-price">${pick('通行證', 'Pass')} <strong>${esc(priceText)}</strong> ${pick('起', 'and up')}</p>` : ''}<div class="dialog-actions"><a class="button" href="#membership">${pick('查看方案與付款', 'Plans & checkout')} ↗</a>${signedIn ? '' : `<button class="button light" data-paywall-login>${pick('登入／註冊', 'Sign in / register')}</button>`}<button class="text-link" data-step="${Number(firstFreeIndex) || 0}">${pick('回到免費第一節', 'Back to the free first section')}</button></div></section>`;
}

/** Strip paid stages for a public export (used by tools, also unit-tested). */
export function publicStubCourse(course, freeStages = settings.freeStagesPerCourse) {
  return {...course, stages: (course.stages || []).map((stage, i) => i < freeStages ? stage : {
    id: stage.id, order: stage.order, title: stage.title, titleEn: stage.titleEn,
    steps: (stage.steps || []).map(s => ({id: s.id, order: s.order, sequence: s.sequence, title: s.title, titleEn: s.titleEn, locked: true, prerequisiteIds: s.prerequisiteIds || [], sourceIds: s.sourceIds || [], knowledge: [], quiz: {question: '', questionEn: '', options: ['', '', ''], optionsEn: ['', '', ''], answer: 0}}))
  })};
}
