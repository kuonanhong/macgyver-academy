/** Transfer learning: curated comparisons stay distinct from automatic suggestions. */
import {placeLocationMarkup} from './course-places.js';
import {projectIconSvg} from './project-identity.js';
let entries = new Map();
let catalogItems = [];
const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const bilingual = (object, key, zh) => object?.[zh ? key : `${key}En`] || object?.[key] || '';
const list = value => Array.isArray(value) ? value : [];
export function safeReference(value) {
  try { const u = new URL(value); return u.protocol === 'https:' && !u.username && !u.password ? u.href : ''; } catch { return ''; }
}
export function setRelatedSkills(data, catalog = []) {
  entries = new Map(list(data?.courses).filter(c=>typeof c?.courseId==='string').map(c=>[c.courseId,c]));
  catalogItems = list(catalog);
}
export function relatedForCourse(course) {
  const curated = entries.get(course.id);
  if (curated) return { ...curated, curated: true };
  // These are catalogue navigation aids, not claims of researched equivalence.
  const candidates = catalogItems.filter(c=>c.id!==course.id && c.category===course.category);
  candidates.sort((a,b)=>Number(!!b.stages)-Number(!!a.stages)||String(a.id).localeCompare(String(b.id)));
  return { courseId:course.id, curated:false, related:candidates.slice(0,6), references:[] };
}
function catalogLink(item, zh) {
  const match = item.id && catalogItems.find(c=>c.id===item.id);
  return match ? `<a class="text-link" href="#project/${encodeURIComponent(match.id)}">${zh?'開啟學習項目':'Open learning topic'} ↗ <small>${match.stages||match.status==='guided'||match.kind==='course' ? (zh?'逐步課程':'Guided course') : (zh?'研究路線圖':'Research roadmap')}</small></a>` : '';
}
function sourceMarkup(reference, zh) {
  const url = safeReference(reference.url); if (!url) return '';
  return `<li><a href="${escape(url)}" target="_blank" rel="noopener">${escape(bilingual(reference,'title',zh))} ↗</a><small>${escape(reference.publisher||new URL(url).hostname)}</small><p>${escape(bilingual(reference,'scope',zh))}</p></li>`;
}
function comparisonMarkup(item, entry, zh) {
  const refs = list(item.referenceUrls).map(url=>list(entry.references).find(r=>r.url===url) || {url,title:new URL(safeReference(url)||'https://invalid.local').hostname});
  const linked=catalogItems.find(c=>c.id===item.id);
  return `<article class="skill-project"><h4>${linked?projectIconSvg(linked,{en:!zh}):''}<span>${escape(bilingual(item,'title',zh))}</span></h4><p><strong>${zh?'相似處與可延伸的原理':'Shared and transferable principles'}</strong><br>${escape(bilingual(item,'transfer',zh))}</p>${catalogLink(item,zh)}${placeLocationMarkup(item.place,{zh,language:zh?'zh-TW':'en'})}<details class="skill-comparison"><summary><span>${zh?'比較差異、三步練習與來源':'Differences, three-step practice and sources'}</span></summary><p class="skill-why">${escape(bilingual(item,'why',zh))}</p><dl><dt>${zh?'必須重新判斷的差異':'Differences that need fresh judgment'}</dt><dd>${escape(bilingual(item,'difference',zh))}</dd></dl><h4>${zh?'三步比較練習':'Three-step comparison exercise'}</h4><ol>${list(bilingual(item,'practice',zh)).map(p=>`<li>${escape(p)}</li>`).join('')}</ol>${refs.length?`<ul class="skill-inline-references">${refs.map(r=>sourceMarkup(r,zh)).join('')}</ul>`:''}</details></article>`;
}
export function relatedSkillsMarkup(course, {zh=true, compact=false}={}) {
  const entry = relatedForCourse(course); if (!entry.related?.length && !entry.references?.length) return '';
  const heading = zh?'從這項工程，學會下一項技能':'Take this engineering knowledge further';
  const body = entry.curated ? `<p>${escape(bilingual(entry,'overview',zh))}</p><p class="subtext">${zh?'先比較相同原理，再確認尺度、材料與驗證方法的差異。比較是原創教學整理；來源支持個別工程與原理，不表示工程之間採用相同商用設計。':'Compare shared principles, then differences in scale, materials and validation. Comparisons are original educational synthesis; sources support individual projects and principles, not claims that projects use identical commercial designs.'}</p><div class="skill-comparisons">${entry.related.map(item=>comparisonMarkup(item,entry,zh)).join('')}</div><details class="skill-reading"><summary>${zh?'本專案新增參考資料與閱讀重點':'Additional references and reading goals'} · ${entry.references.length}</summary><ol>${entry.references.map(ref=>sourceMarkup(ref,zh)).join('')}</ol></details>` : `<p class="subtext">${zh?'依相同領域自動推薦的研究入口；尚未編寫這些項目之間的專屬比較教案，也不臆造未核實的工程地點。':'Automatically suggested research topics in the same discipline; dedicated comparison lessons and locations have not been verified for these relationships.'}</p><div class="skill-topic-grid">${entry.related.map(item=>`<article><h4>${escape(bilingual(item,'title',zh))}</h4><p>${escape(bilingual(item,'summary',zh))}</p>${catalogLink(item,zh)}</article>`).join('')}</div>`;
  return `<section class="related-skills task-card"><span class="task-label">COMPARE · TRANSFER · TEST</span><h3>${heading}</h3>${compact?`<details class="skill-library"><summary>${zh?'展開相關技能與延伸閱讀':'Explore related skills and reading'}</summary>${body}</details>`:body}</section>`;
}
