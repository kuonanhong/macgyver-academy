import { COMPUTING_SUBJECTS, renderComputingVisual, renderComputingIcon } from './computing-visuals.js';
import { hasWorldVisual, renderWorldVisual, renderWorldIcon } from './world-project-visuals.js';
import {PACKAGING_SUBJECTS,renderPackagingVisual} from './packaging-visuals.js';
import {renderPackagingIcon} from './packaging-icons.js';
import {renderSemiconductorVisual,SEMICONDUCTOR_SUBJECTS} from './semiconductor-visuals.js';
import {renderSemiconductorIcon} from './semiconductor-icons.js';
import {ELECTRONICS_SUBJECTS,renderElectronicsVisual,renderElectronicsIcon} from './electronics-visuals.js';
/* Original visual identities for the editorial catalog. These are identifiers,
   not photographs, equipment drawings, engineering diagrams or digital twins. */
const escape = value => String(value ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const disciplines = {
  semiconductor: ['SC', '<circle cx="32" cy="32" r="23"/><path d="M14 20h36M10 32h44M14 44h36M20 11v42M32 9v46M44 11v42"/><path d="M22 54h20"/>'],
  packaging: ['PK', '<path d="m8 21 24-12 24 12-24 12zM8 31l24 12 24-12M8 41l24 12 24-12"/><path d="M16 54v5m11-2v5m10-5v5m11-8v5"/>'],
  electronics: ['EE', '<path d="M4 32h9l5-11 7 22 7-22 7 22 6-11h15M10 12h15m14 0h15M32 5v14M9 52h46"/><circle cx="9" cy="12" r="3"/><circle cx="55" cy="12" r="3"/>'],
  computing: ['IT', '<rect x="20" y="19" width="24" height="24" rx="4"/><path d="M32 5v14M32 43v16M5 32h15M44 32h15M10 10l10 10m24 24 10 10M54 10 44 20M20 44 10 54"/><circle cx="32" cy="31" r="4"/><path d="M28 37h8"/>'],
  instruments: ['OP', '<path d="M29 8q-16 24 0 48M35 8q16 24 0 48M4 16l22 8m12 14 22 10M4 32h56M4 48l22-8m12-14 22-10"/><path d="M30 5h4m-4 54h4"/>'],
  structures: ['BR', '<path d="M5 45h54M17 52V12M47 52V12M5 42l12-24q15 29 30 0l12 24M23 29v13m9-7v7m9-13v13M4 57h56"/>'],
  underground: ['TU', '<path d="M9 55V31a23 23 0 0 1 46 0v24M17 55V31a15 15 0 0 1 30 0v24M22 53l5-16m15 16-5-16M6 8h12m33-1h9M3 20h7m44 0h7"/><path d="M23 46h18"/>'],
  water: ['HY', '<path d="M12 13h38M17 13v39h31L34 13M5 39q6-7 12 0m32 0q5-7 11 0M3 53q7-7 14 0t14 0 14 0 14 0M29 21v20"/><path d="m24 35 5 7 5-7"/>'],
  rail: ['RL', '<rect x="17" y="6" width="30" height="39" rx="8"/><path d="M21 14h22v15H21zM22 54l6-9m14 9-6-9M18 58h29"/><circle cx="25" cy="36" r="2"/><circle cx="39" cy="36" r="2"/>'],
  environment: ['EN', '<path d="M32 57V32M31 42Q8 44 8 16q26 0 24 26M33 33Q35 8 57 8q0 26-24 25M16 24l15 17M49 17 34 31M6 58h52"/>'],
  aerospace: ['AE', '<path d="m32 5 5 23 21 14v7L37 41l-1 12 8 5v3l-12-3-12 3v-3l8-5-1-12L6 49v-7l21-14z"/>'],
  marine: ['MA', '<path d="M5 39h54l-9 13H17zM14 39V23h22v16M36 30h12v9M22 23V8h9v15M3 57q7-6 14 0t14 0 14 0 16 0M22 16h9"/>'],
  automotive: ['AU', '<path d="m8 29 8-14h28l9 14 5 6v13h-6M12 48H6V35zM15 48h33M16 29h28M31 15v14M11 36h8m27 0h7"/><circle cx="17" cy="48" r="6"/><circle cx="47" cy="48" r="6"/>'],
  space: ['SP', '<path d="m26 22 16 4-4 17-16-4zM7 15l14 4-4 17-14-4zM47 32l14 4-4 17-14-4zM17 28l7 2m16 4 6 2M32 25l3-13M28 10q10-4 16 4"/><path d="M10 51q14 12 34 6M48 7q10 4 12 17"/>'],
  manufacturing: ['ME', '<path d="M8 57h48M17 57V43l13-17M34 26l13 10M47 36l7-10M50 20l7 5 3-4M11 44h13"/><circle cx="31" cy="21" r="7"/><circle cx="47" cy="38" r="5"/><circle cx="17" cy="44" r="5"/>'],
  energy: ['PW', '<rect x="13" y="10" width="38" height="46" rx="4"/><path d="M25 10V5h14v5M34 17 23 34h12l-5 15 12-20H30z"/>'],
  materials: ['MT', '<path d="m12 17 20-10 20 10v28L32 57 12 45zM12 17l20 12 20-12M32 29v28M12 45l20-11 20 11M32 7v27"/><circle cx="32" cy="29" r="3"/>'],
  biomedical: ['BM', '<circle cx="32" cy="31" r="23"/><circle cx="32" cy="31" r="14"/><path d="M5 56h54M32 22v18m-9-9h18M32 4v4M5 31h4m46 0h4"/>'],
  process: ['PC', '<path d="M7 10h16v10h-3v20l9 12v5H3v-5l9-12V20H9V10M38 12h18v11H38zM42 23v27h10V23M24 32h18M6 48h18M41 38h12"/>'],
  megascience: ['MS', '<ellipse cx="32" cy="32" rx="26" ry="13"/><ellipse cx="32" cy="32" rx="26" ry="13" transform="rotate(60 32 32)"/><ellipse cx="32" cy="32" rx="26" ry="13" transform="rotate(120 32 32)"/><circle cx="32" cy="32" r="4"/>'],
};
// Subject silhouettes are drawn for each guided course. They show recognizable
// subject families, not scale, exact product geometry or manufacturing details.
const subjects = {
  semiconductor:'<circle cx="32" cy="30" r="23"/><path d="M13 18h38M9 30h46M13 42h38M20 10v40M32 7v46M44 10v40M23 53h18"/><path d="M8 58h48"/>',
  sub2nm:'<path d="M8 18 31 9l25 9-25 9zM8 29l23 9 25-9M8 40l23 9 25-9M8 51l23 9 25-9"/><path d="M19 14v33q0 7 9 7h10q9 0 9-7V14"/>',
  asml:'<path d="M7 56V13h23v9h26v34zM13 18h10v8H13zM15 35h10m4-6 9 7-8 8 13 5M39 25h11M40 50h11M11 56v5m39-5v5"/><ellipse cx="43" cy="50" rx="10" ry="3"/>',
  idf:'<path d="m32 4 5 24 22 19-1 5-19-9 1 9 9 8-17-4-17 4 9-8 1-9-19 9-1-5 22-19zM29 34v20m6-20v20M27 24h10"/>',
  apache:'<path d="M4 15h51M30 11v12M22 24h15l8 16H20l-6-9zM20 31H7L3 21M8 18v15M45 34l14 1M22 40l-3 10h27M26 48v-7m14 7v-7M25 28h8l4 7H22"/>',
  submarine:'<path d="M5 37q2-13 19-13h24l11 13-11 11H24Q7 48 5 37zM27 24V13h11v11M30 13V7h9M53 31l7-7v25l-7-7M18 31h3m5 0h3m5 0h3M8 55h45"/>',
  danjiang:'<path d="M4 44h56M36 54V7l8 47M5 44 36 13 14 44m10 0 12-31 16 31m8 0L36 13M3 57q7-4 14 0t14 0 14 0 14 0"/>',
  hsuehshan:'<path d="m3 30 14-17 11 10L43 5l18 25M8 56V43a11 11 0 0 1 22 0v13M35 56V43a11 11 0 0 1 22 0v13M13 55l4-16m8 16-4-16m19 16 4-16m8 16-4-16M6 60h54"/>',
  cybersecurity:'<path d="m32 6 18 8v16q0 18-18 26Q14 48 14 30V14zM24 30l6 6 11-15M3 13h11M3 48h14M50 13h11M47 48h14"/><circle cx="4" cy="13" r="2"/><circle cx="4" cy="48" r="2"/><circle cx="60" cy="13" r="2"/><circle cx="60" cy="48" r="2"/>',
  packaging:'<path d="m6 34 26-11 26 11-26 11zM6 43l26 11 26-11M6 51l26 10 26-10M13 23l12-6 12 6-12 5zM32 15l12-6 11 6-11 5zM13 23v8l12 5 12-5v-8m-5-8v8l12 5 11-5v-8"/>',
  'silicon-photonics':'<path d="M8 16h48v32H8zM0 32h15M15 32q8 0 12-9h16M15 32q8 0 12 9h16M43 23h18M43 41h18M18 21v22M27 52v8m11-8v8"/><circle cx="47" cy="23" r="3"/><circle cx="47" cy="41" r="3"/>',
  'steam-locomotive':'<path d="M7 44V25h31v19M10 25V13h9v12M36 44V14h18v30M40 20h10v11H40zM4 44h56M6 50h46M54 42l7 8M14 9q-7-5 1-8M24 18h6v7"/><circle cx="15" cy="48" r="8"/><circle cx="34" cy="48" r="8"/><circle cx="51" cy="49" r="5"/><path d="M15 48h19"/>',
  ferrari:'<path d="m5 36 10-4 12-12h14l10 13 8 4v10h-8M14 47h28M5 47H2V37zM22 32h23M31 21l-3 11M7 37h9m35-1h6"/><circle cx="14" cy="47" r="7"/><circle cx="49" cy="47" r="7"/><path d="M6 57h51"/>',
  tesla:'<path d="m5 32 11-15h26l12 15 6 8v9h-6M13 49H4V38zM16 32h32M32 18v14M20 49h21M8 37h7m34 0h7"/><circle cx="16" cy="49" r="7"/><circle cx="48" cy="49" r="7"/><path d="M24 40h16v5H24zM29 36l-2 4h5l-2 5"/>',
  starlink:'<path d="M5 10h19v38H5zM11 10v38m7-38v38M5 20h19M5 30h19M5 40h19M24 29h12M36 24l22-7 3 22-22 7zM40 29l15-5M41 36l15-5M37 45l-4 8M51 43l6 6M9 56q19 7 36 0"/>',
  'three-gorges':'<path d="M4 19h56M8 19v33h48V19M4 52h56M10 25h44M16 25v27m8-27v27m8-27v27m8-27v27m8-27v27M2 59q8-5 16 0t16 0 16 0 14 0M3 13h20m17 0h20"/>',
  metro:'<rect x="12" y="5" width="31" height="43" rx="9"/><path d="M17 13h21v17H17zM27 13v17M16 40h23M16 57l8-9m17 9-8-9M11 61h35M53 17v42"/><circle cx="20" cy="36" r="2"/><circle cx="35" cy="36" r="2"/><rect x="47" y="6" width="12" height="21" rx="4"/><circle cx="53" cy="12" r="2"/><circle cx="53" cy="21" r="2"/>',
  a004:'<ellipse cx="31" cy="43" rx="26" ry="12"/><path d="M5 43v7q26 20 52 0v-7M19 29v13q12 9 25 0V29M26 7h10v12M13 12q-10 7-5 17m-4-3 4 3 4-4M43 13l10 7-5 10"/><ellipse cx="31" cy="29" rx="13" ry="7"/>',
  a106:'<ellipse cx="32" cy="17" rx="25" ry="9"/><path d="M7 17v5q25 18 50 0v-5M7 43v5q25 18 50 0v-5M18 27v10m14-7v7m14-10v10M13 7v-4m38 4V3"/><ellipse cx="32" cy="43" rx="25" ry="9"/><path d="m27 33 5 5 5-5"/>',
  a405:'<path d="M25 6q-13 26 0 52M25 6q14 26 0 52M29 7q16 25 0 50M35 7q5 25 0 50M3 15l18 8m16 13 23 13M3 49l18-8m16-13 23-13M3 32h57"/>',
  a310:'<rect x="9" y="14" width="43" height="40" rx="3"/><path d="M14 8v6m9-6v6m9-6v6m9-6v6M15 54v7m11-7v7m12-7v7m10-7v7M3 21h6m-6 11h6m-6 11h6m43-22h9m-9 11h9m-9 11h9M24 31v-5a8 8 0 0 1 16 0v5"/><rect x="20" y="31" width="24" height="17" rx="3"/><circle cx="32" cy="38" r="2"/><path d="M32 40v4"/>',
  a203:'<rect x="14" y="26" width="36" height="28" rx="2"/><path d="M6 32h8M6 38h8M6 44h8M6 50h8M50 32h8m-8 6h8m-8 6h8m-8 6h8M21 26V8m11 18V5m11 21V8M16 12h10m-10 6h10m1-9h10m-10 6h10m1-3h10m-10 6h10M10 59h46"/><circle cx="23" cy="55" r="3"/><circle cx="43" cy="55" r="3"/>',
  b003:'<path d="M3 46h58M15 57V9M48 57V9M3 43l12-29q17 31 33 0l13 29M22 25v18m10-12v12m10-18v18M14 20h4m-4 11h4m28-11h4m-4 11h4M4 60h57"/>',
  b102:'<path d="M3 12q7-5 14 0t14 0 14 0 16 0M3 25h58M4 54V44a10 10 0 0 1 20 0v10M40 54V44a10 10 0 0 1 20 0v10M27 54V45a5 5 0 0 1 10 0v9M24 47h3m10 0h3M9 53l2-10m8 10-2-10M44 53l3-10m9 10-3-10"/>',
  b202:'<path d="m4 9 7 22-3 27m52-49-7 22 3 27M10 14q22 16 44 0M15 20l7 36q10 7 20 0l7-36M22 55q10 6 20 0M23 26l5 23m13-23-5 23M12 14V5m41 9V5M7 5h10m31 0h10M4 61q7-4 14 0t14 0 14 0 14 0"/>',
  b301:'<path d="M5 47q6-23 32-24h22v24zM21 35q5-8 15-8v8zM40 27h6v8h-6zm10 0h6v8h-6zM4 42h55M6 53h53M9 59h48M23 47v6m26-6v6M3 19h29M8 12h27"/>',
  b401:'<path d="M3 32h9m12 0h8m13 0h8M12 14h12v37H12zM32 18h13v32H32zM53 11h8v44h-8zM15 21v23m6-23v23M37 22v24m3-24v24M57 18v30M49 19l3 3m-3 20 3-3"/>',
  c001:'<path d="m32 3 4 22 23 12v7l-22-7-1 17 8 6-12-3-12 3 8-6-1-17-22 7v-7l23-12zM25 32l-4 11m18-11 4 11M28 17h8M13 36l-4-4m46 4 4-4"/><ellipse cx="20" cy="42" rx="3" ry="6"/><ellipse cx="44" cy="42" rx="3" ry="6"/>',
  c101:'<path d="M9 46h43l-5-17H20zM13 46v9h41M22 46v9m22-9v9M16 36l-9 7 4 6m35-12 12 6-2 8M30 9v9M21 17h20"/><circle cx="33" cy="30" r="12"/><circle cx="33" cy="30" r="5"/><path d="M12 58h46"/>',
  c213:'<path d="m4 37 17-17h20l17 18v10h-9M14 48H4V37M22 48h19M15 34h34M28 21l-4 13M8 39h7m36 0h6"/><circle cx="17" cy="48" r="7"/><circle cx="46" cy="48" r="7"/><path d="M22 11h23m-5-4 5 4-5 4M39 59H20m5-4-5 4 5 4"/>',
  c307:'<path d="M4 10h23v27H4zM12 10v27m8-27v27M4 19h23m-23 9h23M27 24h10M37 13h17v28H37zM41 13V7h9v6M40 41l-4 11m14-11 6 11M30 59q15-11 30 0"/><circle cx="45" cy="33" r="5"/><path d="M42 38l-6 14m12-14 8 14"/>',
  c407:'<path d="M7 58h43M17 54V39l11-17M33 22l15 14M49 36l5-13M53 20l7 3M51 20l3-7m6 10 2-7"/><circle cx="17" cy="42" r="7"/><circle cx="31" cy="18" r="7"/><circle cx="48" cy="39" r="6"/><circle cx="54" cy="21" r="3"/><path d="M12 53h13v5"/>',
  d002:'<path d="M4 15h39v7H4zM8 22v22h32V22M15 22v22m8-22v22m8-22v22M8 44h32l16 12M40 44l14-17M43 15h9v17M4 55h24M4 60h44"/><circle cx="47" cy="44" r="9"/><path d="M47 36v16m-7-8h15m-12-5 9 11m-1-12-9 11"/>',
  d107:'<path d="M9 57V23h17v34M9 23l8-12 9 12M17 11V5M26 34h13M39 20h19v31H39zM43 25v20m5-20v20m5-20v20M40 51v7H18M5 58h24M14 30h7m-7 7h7m-7 7h7"/><circle cx="49" cy="10" r="7"/><path d="M46 7v6m6-6v6m-6-3h6"/>',
  d201:'<rect x="8" y="8" width="38" height="42" rx="4"/><circle cx="27" cy="29" r="12"/><path d="M13 50v9m27-9v9M23 31h34v8H23zM50 39v18m-6 0h16M23 19v3m-6 7h3m14 0h3M27 43v3"/>',
  d310:'<path d="M4 22v-9l8 4v-4l8 4v13H4zM12 13V5h5v11M42 30V19l8 4v-4l10 4v15H42zM49 20V9h5v13M22 60V47l9 4v-4l9 4v9zM9 37q0 14 9 16m-3-4 3 4-5 1M26 13q13-5 21 2m-5 0h5v-5M53 43q-2 11-10 12m5-4-5 4 4 4"/>',
  d401:'<ellipse cx="32" cy="31" rx="27" ry="21"/><ellipse cx="32" cy="31" rx="21" ry="15"/><circle cx="8" cy="31" r="4"/><circle cx="56" cy="31" r="4"/><circle cx="32" cy="12" r="4"/><circle cx="32" cy="50" r="4"/><path d="M26 25l12 12m-12 0 12-12M4 58h56"/>',
  b015:'<path d="M3 46h58M16 57V7h4v50M44 57V7h4v50M3 43 18 13q14 29 28 0l15 30M18 18h28M17 27h3m24 0h3M17 37h3m24 0h3M26 26v17m6-13v13m6-17v17M4 60h55"/>',
  b021:'<path d="M32 3v7M26 10h12l-2 7h-8zM25 17h14l-2 8H27zM23 25h18l-2 8H25zM21 33h22l-2 8H23zM19 41h26l-2 8H21zM17 49h30l-2 8H19zM13 57h38v5H13zM30 14h4m-5 7h6m-7 8h8m-9 8h10m-11 8h12m-13 8h14"/>',
  b103:'<path d="M2 25 17 6l12 14L41 4l21 23M4 57V43a12 12 0 0 1 24 0v14M36 57V43a12 12 0 0 1 24 0v14M28 46h8M10 53h11M42 53h12M13 46h5v7h-5m31-7h7v7h-7M7 61h51M31 28v6"/>',
  b226:'<path d="M4 9h56M5 14h16v16h19v16h19M5 21h16v16h19v16h19M21 14v23m19-7v23M5 57h54M9 25l3 5h6l3-5zM26 40l3 5h6l3-5zM45 54l3 4h7l3-4zM48 15h10v7H48zM47 28h11v7H47z"/>',
  a025:'<path d="m6 26 26-12 26 12-26 12zM6 35l26 12 26-12M6 44l26 12 26-12M17 21v13m14-19v19m14-14v14M12 49v9m10-5v8m10-5v8m10-11v8m10-13v9M6 61h52M16 9h32"/>',
  a042:'<path d="M6 9h19M8 11l10 21 26-15-4 23-9 13M9 30q10 9 20 0M33 17q11-9 21 0M30 39q10 8 20 0M21 53h29M26 44l8 9 8-9M7 59h49"/><path d="M28 7h9m-9 3h9"/>',
  a211:'<rect x="8" y="19" width="15" height="26" rx="2"/><rect x="41" y="19" width="15" height="26" rx="2"/><path d="M2 32h6m15-6h18M23 38h18M56 32h6M13 26l5 6-5 6m34-12 5 6-5 6M13 12V6m-4 6h8m30 0V6m-4 6h8M5 53h54M29 17h6M29 47h6"/>',
  a319:'<path d="M32 10 10 28l9 25h26l9-25zM32 10l13 43M32 10 19 53M10 28h44"/><circle cx="32" cy="10" r="6"/><circle cx="10" cy="28" r="6"/><circle cx="19" cy="53" r="6"/><circle cx="45" cy="53" r="6"/><circle cx="54" cy="28" r="6"/><path d="M29 9l2 2 4-4M7 27l2 2 4-4M16 52l2 2 4-4"/>',
  c005:'<path d="m32 3 4 23 24 10-2 8-21-7-1 16 8 7-12-3-12 3 8-7-1-16-21 7-2-8 24-10zM24 34l-4 9m20-9 4 9M15 36l-4-5m38 5 4-5"/><ellipse cx="20" cy="42" rx="4" ry="6"/><ellipse cx="44" cy="42" rx="4" ry="6"/><path d="M31 17l-3 5h7l-3 5"/>',
  c325: '',
  d036:'<path d="M15 28v28M44 21v34M15 28l-1-19m1 19L3 37m12-9 16 9M44 21V3m0 18L28 30m16-9 16 9M3 48q7-5 14 0t14 0 14 0 16 0M15 57h29l13 3M9 62h42"/><circle cx="15" cy="28" r="3"/><circle cx="44" cy="21" r="3"/>',
  d202:'<path d="M17 10h31q13 0 13 20T48 50H17M29 10q13 20 0 40M41 10q13 20 0 40M17 50v9m33-9v9M8 59h50M3 34h34v6H3zM6 40v15M12 30h22"/><ellipse cx="17" cy="30" rx="12" ry="20"/><ellipse cx="17" cy="30" rx="7" ry="13"/><circle cx="8" cy="29" r="3"/>',
};
// Eighteen original hexagonal mirror segments, with a central clearance, above
// five stylized sunshield layers identify Webb without copying mission artwork.
subjects.c325=Array.from({length:5},(_,row)=>row-2).flatMap(row=>Array.from({length:5},(_,col)=>col-2).filter(col=>Math.abs(row+col)<=2&&(row!==0||col!==0)).map(col=>{const x=31+col*9+row*4.5,y=23+row*7.8;return '<path d="'+Array.from({length:6},(_,i)=>{const a=(i*60+30)*Math.PI/180;return(i?'L':'M')+(x+5*Math.cos(a)).toFixed(2)+' '+(y+5*Math.sin(a)).toFixed(2)}).join('')+'Z"/>'})).join('')+Array.from({length:5},(_,i)=>`<path d="M4 ${47+i*2.5}l26-6 30 6-30 7z"/>`).join('');
const subjectMotif=course=>subjects[course.id]||motif(course.category);
export const projectIdentitySubjectIds=Object.freeze([...new Set([...Object.keys(subjects),...Object.keys(SEMICONDUCTOR_SUBJECTS),...Object.keys(PACKAGING_SUBJECTS)])]);
const hues=[146,157,181,205,224,32,45,193,164,112,202,190,12,235,28,72,14,178,39,257];
const keys=Object.keys(disciplines);
// Concrete hex colours also render correctly in exported SVG and older viewers.
const identityColor=(h,s,l)=>{s/=100;l/=100;const a=s*Math.min(l,1-l),f=n=>{const k=(n+h/30)%12;return Math.round(255*(l-a*Math.max(-1,Math.min(k-3,9-k,1)))).toString(16).padStart(2,'0')};return '#'+f(0)+f(8)+f(4)};
const hash=value=>{let n=2166136261;for(const c of String(value)){n^=c.codePointAt(0);n=Math.imul(n,16777619)}return n>>>0};
const titleFor=(course,en)=>en?(course.titleEn||course.title||course.id):(course.title||course.titleEn||course.id);
const motif=category=>(disciplines[category]||disciplines.manufacturing)[1];
export function domainIconSvg(category,{title='',decorative=false}={}) {
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" class="domain-icon" ${decorative?'aria-hidden="true"':`role="img" aria-label="${escape(title||category)}"`}><g fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">${motif(category)}</g></svg>`;
}
export function projectIconSvg(course,{en=false}={}) {
  if(COMPUTING_SUBJECTS[course.id]) return renderComputingIcon(course.id,{en,zh:!en});
  if(hasWorldVisual(course)) return renderWorldIcon(course,{en});
  if(ELECTRONICS_SUBJECTS[course.id]) return renderElectronicsIcon(course.id,{en});
  if(PACKAGING_SUBJECTS[course.id]) return renderPackagingIcon(course.id,{en});
  if(SEMICONDUCTOR_SUBJECTS[course.id]) return renderSemiconductorIcon(course.id,{en});
  const id=String(course.id||'project'),n=hash(id),hue=hues[Math.max(0,keys.indexOf(course.category))];
  const points=Array.from({length:12},(_,i)=>{const angle=(i*30-90)*Math.PI/180,r=35+(n>>>(i%24)&1)*4;return `${(44+Math.cos(angle)*r).toFixed(2)},${(44+Math.sin(angle)*r).toFixed(2)}`}).join(' ');
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 88 104" class="project-icon" role="img" aria-label="${escape(titleFor(course,en))} · ${en?'original project emblem':'原創專案識別'}" data-project-icon="${escape(id)}" data-subject-art="${subjects[id]?escape(id):'domain-identity'}"><polygon points="${points}" fill="${identityColor(hue,25,93)}" stroke="${identityColor(hue,28,38)}" stroke-width="1.5"/><g transform="translate(20 18) scale(.75)" fill="none" stroke="#315344" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">${subjectMotif(course)}</g><text x="44" y="98" text-anchor="middle" font-family="ui-monospace,monospace" font-size="${id.length>14?6:8}" fill="#244a36">${escape(id.toUpperCase())}</text></svg>`;
}
export function projectIdentitySvg(course,{en=false}={}) {
  if(COMPUTING_SUBJECTS[course.id]) return renderComputingVisual(course.id,{zh:!en}).replace('class="computing-subject-visual"','class="computing-subject-visual project-identity"').replace('<svg ','<svg data-project-identity="'+escape(course.id)+'" data-subject-art="'+escape(course.id)+'" ');
  if(hasWorldVisual(course)) return renderWorldVisual(course,{zh:!en}).replace('class="world-project-visual"','class="world-project-visual project-identity"').replace('<svg ','<svg data-project-identity="'+escape(course.id)+'" data-subject-art="'+escape(course.id)+'" ');
  if(ELECTRONICS_SUBJECTS[course.id]) return renderElectronicsVisual(course.id,{zh:!en}).replace('class="electronics-subject-visual"','class="project-identity"').replace('<svg ','<svg data-project-identity="'+escape(course.id)+'" data-subject-art="'+escape(course.id)+'" ');
  if(PACKAGING_SUBJECTS[course.id]) return renderPackagingVisual(course.id,{zh:!en}).replace('class="packaging-subject-visual"','class="project-identity"').replace('<svg ','<svg data-project-identity="'+escape(course.id)+'" data-subject-art="'+escape(course.id)+'" ');
  if(SEMICONDUCTOR_SUBJECTS[course.id]) return renderSemiconductorVisual(course.id,{zh:!en}).replace('class="semiconductor-subject-visual"','class="project-identity"').replace('<svg ','<svg data-project-identity="'+escape(course.id)+'" data-subject-art="'+escape(course.id)+'" ');
  const id=String(course.id||'project'),n=hash(id),category=course.category||'manufacturing',i=Math.max(0,keys.indexOf(category)),hue=hues[i],code=(disciplines[category]||disciplines.manufacturing)[0];
  const cells=Array.from({length:32},(_,j)=>`<rect x="${29+(j%8)*8}" y="${201+Math.floor(j/8)*8}" width="5" height="5" fill="${n>>>(j%32)&1?'#476855':'#c5d3bf'}"/>`).join('');
  const spokes=Array.from({length:12},(_,j)=>{const a=(j*30+(n%19))*Math.PI/180,r=84+(n>>>(j%24)&1)*9;return `<path d="M${(260+Math.cos(a)*79).toFixed(2)} ${(130+Math.sin(a)*79).toFixed(2)}L${(260+Math.cos(a)*r).toFixed(2)} ${(130+Math.sin(a)*r).toFixed(2)}"/>`}).join('');
  return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 520 270" class="project-identity" role="img" aria-label="${escape(titleFor(course,en))} · ${en?'original catalog illustration, not an engineering drawing':'原創目錄插畫，非工程圖'}" data-project-identity="${escape(id)}" data-subject-art="${subjects[id]?escape(id):'domain-identity'}"><rect width="520" height="270" fill="${identityColor(hue,24,94)}"/><path d="M0 54h520M0 216h520M104 0v270M416 0v270" stroke="#8ba48b" stroke-opacity=".15"/><circle cx="260" cy="130" r="95" fill="none" stroke="#9eaf96" stroke-width=".8"/><circle cx="260" cy="130" r="75" fill="${identityColor(hue,27,87)}"/><g stroke="#597657" stroke-width="2">${spokes}</g><g transform="translate(196 66) scale(2)" fill="none" stroke="#315344" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">${subjectMotif(course)}</g><text x="26" y="30" font-family="ui-monospace,monospace" font-size="12" letter-spacing="2" fill="#315344">${escape(code)} / ${escape(id.toUpperCase())}</text><text x="490" y="31" text-anchor="end" font-family="ui-monospace,monospace" font-size="10" fill="#52694d">MACGYVER</text>${cells}<text x="493" y="247" text-anchor="end" font-family="ui-monospace,monospace" font-size="9" letter-spacing="1" fill="#52694d">${en?'ORIGINAL PROJECT IDENTITY':'原創專案識別插畫'}</text></svg>`;
}
export function domainIdentitySvg(category,{title=category,en=false}={}) {
  return projectIdentitySvg({id:category,category,title,titleEn:title},{en})
    .replace('data-project-identity=', 'data-domain-identity=')
    .replace('original catalog illustration, not an engineering drawing','original discipline illustration, not an engineering drawing')
    .replace('原創目錄插畫，非工程圖','原創領域插畫，非工程圖')
    .replace('ORIGINAL PROJECT IDENTITY','ORIGINAL DISCIPLINE IDENTITY')
    .replace('原創專案識別插畫','原創領域識別插畫');
}
export function projectMediaMarkup(course,{photo=null,en=false,compact=false}={}) {
  const label=photo?(en?'Licensed reference photo':'授權參考照片'):(course.educationEdition===11?(en?'Original educational architecture':'原創教學架構圖'):(en?'Original identity illustration':'原創識別插畫'));
  const src=photo?.path;
  const safePath=typeof src==='string'&&/^(?:assets\/|\.\/assets\/)/.test(src)&&!src.split('/').includes('..')?src:null;
  if(photo&&safePath)return `<div class="project-media ${compact?'compact':''}" data-media-kind="photo"><img loading="lazy" src="${escape(safePath)}" alt="${escape(en?(photo.titleEn||photo.title):(photo.title||photo.titleEn))}"><span class="project-media-kind">${label}</span>${compact?'':`<span class="image-credit">${escape(photo.author)} · ${escape(photo.license)}</span>`}<span class="project-photo-emblem">${projectIconSvg(course,{en})}</span></div>`;
  return `<div class="project-media ${compact?'compact':''}" data-media-kind="illustration">${projectIdentitySvg(course,{en})}<span class="project-media-kind">${en?'Original identity illustration':'原創識別插畫'}</span></div>`;
}
export const projectIdentityDomains=Object.freeze([...keys]);
