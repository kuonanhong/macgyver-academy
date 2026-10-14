import {SEMICONDUCTOR_SUBJECTS} from './semiconductor-visuals.js';
// Original pictograms for process families. Shared process families deliberately
// share a glyph; course IDs and accessible titles identify individual courses.
const esc=value=>String(value??'').replace(/[&<>"']/g,char=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[char]));
const glyphs=Object.freeze({
 wafer:'<circle cx="32" cy="31" r="22"/><path d="M15 18h34M11 31h42M15 44h34M20 12v38M32 9v44M44 12v38M25 53h14"/>',
 polish:'<ellipse cx="32" cy="44" rx="25" ry="10"/><path d="M20 14h24v17H20zM26 8h12v6"/><ellipse cx="32" cy="33" rx="14" ry="5"/><path d="M54 16c6 8 6 17 0 23m-2-9 2 9 8-2"/>',
 epitaxy:'<path d="M9 34h46" stroke="#b38948"/><path d="M14 16h36M14 27h36M14 41h36M14 52h36M14 16v36M26 16v36M38 16v36M50 16v36"/><g fill="#315344"><circle cx="14" cy="16" r="3"/><circle cx="38" cy="27" r="3"/><circle cx="26" cy="41" r="3"/><circle cx="50" cy="52" r="3"/></g>',
 soi:'<path d="M8 15h48v10H8zM8 37h48v16H8z"/><path d="M8 26h48v10H8z" fill="#d9c38c"/><path d="M16 31h6m6 0h8m6 0h6"/>',
 clean:'<path d="M9 32v23h46V32M9 42q7-6 15 0t16 0t15 0M32 6c-4 7-11 14-11 21a11 11 0 0 0 22 0c0-7-7-14-11-21z"/><path d="M30 22c-4 5-4 8-1 11"/>',
 fab:'<path d="M8 35V19l16 9V17l16 10V16l16 9v31H8zM15 41h8v8h-8zM30 41h8v8h-8zM45 41h5v8h-5zM45 17V7h7v14"/>',
 oxide:'<rect x="7" y="16" width="50" height="33" rx="11"/><path d="M17 22v21m8-21v21m8-21v21m8-21v21m8-21v21M2 31h6m48 0h6"/>',
 ald:'<path d="M9 48h46v8H9zM14 39h36"/><circle cx="18" cy="17" r="8"/><circle cx="46" cy="17" r="8"/><path d="M27 17h9m-4-4 4 4-4 4M18 27v9m-4-4 4 4 4-4M46 27v9m-4-4 4 4 4-4"/><circle cx="17" cy="42" r="3" fill="#d9c38c"/><circle cx="32" cy="42" r="3"/><circle cx="47" cy="42" r="3" fill="#d9c38c"/>',
 implant:'<path d="M8 39h48v16H8zM14 7v25m-4-5 4 5 4-5M32 7v25m-4-5 4 5 4-5M50 7v25m-4-5 4 5 4-5"/><g fill="#b38948" stroke="none"><circle cx="16" cy="46" r="3"/><circle cx="31" cy="49" r="3"/><circle cx="47" cy="45" r="3"/></g>',
 anneal:'<path d="M8 45h48v10H8zM16 37c-9-9 9-13 0-22M32 37c-9-9 9-13 0-22M48 37c-9-9 9-13 0-22"/><path d="M8 7h48" stroke="#b38948"/>',
 gate:'<path d="M7 41h50v14H7zM12 32h10v9H12zM42 32h10v9H42zM26 29h12v10H26zM24 12h16v17H24zM32 6v6M17 23v9m30-9v9"/>',
 nanosheet:'<rect x="23" y="8" width="20" height="46" rx="8" fill="#d9c38c"/><path d="M7 18h50v6H7zM7 30h50v6H7zM7 42h50v6H7z" fill="#edf4e7"/>',
 backside:'<path d="M8 28h48v10H8zM9 9h16v7H9zM39 9h16v7H39zM17 16v12m30-12v12M26 38v13m13-13v13M8 51h48v7H8z"/><path d="M33 40v8" stroke="#b38948"/>',
 spin:'<ellipse cx="32" cy="41" rx="22" ry="10"/><path d="M26 9h12v9H26zM32 20v10m-3-4 3 4 3-4M7 25c-7 13 0 29 14 32m-7-7 7 7-9 2M52 24c6 5 9 12 7 19"/>',
 resist:'<path d="M7 43h50v12H7zM7 33h50v10H7z" fill="#d9c38c"/><path d="M15 8v17m-4-4 4 4 4-4M32 8v17m-4-4 4 4 4-4M49 8v17m-4-4 4 4 4-4"/><circle cx="22" cy="38" r="2"/><circle cx="42" cy="38" r="2"/>',
 mask:'<rect x="9" y="8" width="46" height="46" rx="2"/><path d="M17 17h26v8H30v21H17z" fill="#bdd0b2"/><path d="M37 34h10v12H37zM4 8h5M55 54h5"/>',
 litho:'<path d="M9 8h46v7H9zM15 15 26 31l-8 20m31-36L38 31l8 20M10 54h44"/><ellipse cx="32" cy="32" rx="18" ry="5" fill="#c0d8d2"/>',
 pattern:'<path d="M8 51h48M16 51V17h10v34m12 0V17h10v34"/><path d="M10 51V17h4m14 0h4v34m0 0V17h4m14 0h4v34" stroke="#b38948"/>',
 etch:'<path d="M8 33h12v18h9V33h9v18h9V33h9v24H8zM8 26h12v7H8zM29 26h9v7h-9zM47 26h9v7h-9zM24 7v14m-3-4 3 4 3-4M42 7v14m-3-4 3 4 3-4"/>',
 plasma:'<rect x="8" y="8" width="48" height="48" rx="9"/><ellipse cx="32" cy="29" rx="17" ry="10" fill="#ddd0c5"/><path d="M16 46h32M19 24l4 4m18-5-3 4m-10 5 4-5m9 10-4-3"/>',
 cvd:'<path d="M8 56V16h48v40M24 7h16v9M16 23h32M16 45h32v7H16zM21 29v10m-3-4 3 4 3-4M32 29v10m-3-4 3 4 3-4M43 29v10m-3-4 3 4 3-4"/>',
 pvd:'<path d="M8 56V8h48v48M17 14h30v7H17zM15 47h34v7H15zM24 27l-9 14m2-6-2 6 6-2M32 27v14m-4-5 4 5 4-5M40 27l9 14m-6-2 6 2-2-6"/>',
 interconnect:'<path d="M7 9h33v10H7zM25 19h10v21H25zM25 40h32v10H25zM8 55h48" fill="#d9c38c"/>',
 cmp:'<path d="M18 8h28v16H18zM32 24v7M9 37h12v5h13v-5h21M9 49h46"/><path d="M50 9c-5 6-6 8-6 11a6 6 0 0 0 12 0c0-3-1-5-6-11"/><path d="M22 30h20" stroke="#b38948"/>',
 reliability:'<path d="M32 7 53 15v16c0 12-10 21-21 27C21 52 11 43 11 31V15z"/><path d="M18 33h9l5-12 7 21 4-9h5" stroke="#b38948"/>',
 dram:'<path d="M11 14v36m-4-26h8m-8 15h8M15 22h9v19h-9M24 31h16M40 17v29m8-29v29M48 31h10M19 14v8m0 19v11"/>',
 nand:'<path d="M10 12h44v7H10zM10 27h44v7H10zM10 42h44v7H10z" fill="#d9c38c"/><path d="M25 6h7v49h-7zM39 6h7v49h-7z" fill="#bfd7d0"/>',
 memory:'<path d="M12 10h40v9H12zM12 44h40v9H12zM18 19h28v25H18z"/><path d="M22 37 30 25l5 12 7-12" stroke="#b38948"/>',
 sensor:'<path d="M10 25h44v29H10zM25 25v29m15-29v29M10 39h44M9 8l8 10m-6-1 6 1-1-6M30 7l8 10m-6-1 6 1-1-6M46 8l8 10m-6-1 6 1-1-6"/>',
 power:'<path d="M9 38h46v17H9zM9 28h46v10H9zM13 19h9v9h-9zM42 19h9v9h-9z"/><path d="m36 5-12 15h9l-5 14 14-18h-9z" fill="#d9c38c"/>',
 mems:'<rect x="23" y="18" width="18" height="29" rx="2" fill="#d9c38c"/><path d="M6 23v20m52-20v20M6 33h4l3-9 4 18 4-9h2M41 33h3l3-9 4 18 4-9h3"/>',
 tft:'<path d="M7 48h50v8H7zM9 35h46v8H9zM13 22h11v13H13zM40 22h11v13H40zM26 43h12v5H26z"/><path d="M15 17h34" stroke="#b38948"/>',
 sem:'<path d="M24 7h16v8H24zM22 15h20l-6 15h-8zM32 31v13m-4-4 4 4 4-4M12 50h34M39 43l13-15M48 18h11v11H48z"/>',
 optical:'<path d="M8 49h48v7H8zM11 14l20 30 21-30M31 11v28"/><path d="m27 39 4 5-1-7m17-18 5-5-1 7"/><rect x="5" y="6" width="12" height="9"/><rect x="47" y="6" width="12" height="9"/>',
 spc:'<path d="M9 9v47h48M13 17h41m-41 29h41"/><path d="m14 37 8-8 8 6 8-9 8 4 8-19" stroke="#b38948"/>',
 test:'<ellipse cx="31" cy="46" rx="24" ry="11"/><path d="M14 8h36v12H14zM20 20v14l-5 8m17-22v14l-5 8m17-22v14l-5 8"/>'
});
export const semiconductorIconFamilies=Object.freeze(Object.keys(glyphs));
export function renderSemiconductorIcon(courseId,{en=false}={}){
 const subject=SEMICONDUCTOR_SUBJECTS[courseId];if(!subject||!glyphs[subject.family])return '';
 const title=en?subject.titleEn:subject.title,description=en?'Original process-family pictogram, not a fabrication drawing. Related processes may share a symbol.':'原創製程類型圖示，非製造圖；相近工法共用類型符號。';
 return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 88 104" class="project-icon" role="img" aria-label="${esc(title+' · '+courseId+' · '+description)}" data-project-icon="${esc(courseId)}" data-subject-art="${esc(courseId)}" data-icon-family="${esc(subject.family)}"><title>${esc(title)}</title><desc>${esc(description)}</desc><rect x="4" y="4" width="80" height="82" rx="15" fill="#edf3e6" stroke="#91a78b" stroke-width="1.4"/><g transform="translate(12 12)" data-icon-geometry="${esc(subject.family)}" fill="none" stroke="#315344" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">${glyphs[subject.family]}</g><text x="44" y="99" text-anchor="middle" font-family="ui-monospace,monospace" font-size="${courseId.length>8?6.5:9}" fill="#244a36">${esc(courseId.toUpperCase())}</text></svg>`;
}
