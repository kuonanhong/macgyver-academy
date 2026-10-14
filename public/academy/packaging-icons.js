import {PACKAGING_SUBJECTS} from './packaging-visuals.js';
// Original compact pictograms, intentionally shared by related physical mechanisms.
const e=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const glyphs={
 stack:'M7 21h50v9H7zM7 37h50v9H7zM15 30v7m17-7v7m17-7v7M17 12v9m15-9v9m15-9v9',
 pillar:'M5 49h54v8H5zM10 25h9v24h-9zM28 25h9v24h-9zM46 25h9v24h-9zM10 25q5-16 9 0m9 0q5-16 9 0m9 0q5-16 9 0',
 bond:'M7 11h50v13H7zM7 43h50v13H7zM16 24v6m16-6v6m16-6v6M16 37v6m16-6v6m16-6v6M32 29v9m-4-4 4 4 4-4',
 wafer:'M7 16c0-13 50-13 50 0s-50 13-50 0zM7 47c0-13 50-13 50 0s-50 13-50 0zM32 27v10m-4-4 4 4 4-4',
 transfer:'M9 11h46v9H9zM16 25h10v8H16zM37 25h10v8H37zM32 33v11m-4-4 4 4 4-4M7 49h50v9H7z',
 grind:'M9 48h46v9H9zM18 10h28v9H18zM21 19h22v16H21zM24 35v6m8-6v6m8-6v6M11 16q-7 12 0 22',
 laser:'M27 7h10v12H27zM25 22l7 24 7-24M6 40h21m10 0h21M6 57h52M30 44l5 5-7 8',
 dice:'M7 30h12v23h7V30h12v23h7V30h12v28H7zM22 7v17m-4-4 4 4 4-4M42 7v17m-4-4 4 4 4-4',
 pick:'M27 7h10v18l9 10H18l9-10zM22 40h20v8H22zM9 58h46M46 21l10-10m-7 0h7v7',
 underfill:'M9 15h46v14H9zM9 46h46v10H9zM18 33v10m14-10v10m14-10v10M5 37h34m-5-4 5 4-5 4',
 warp:'M6 25q26-18 52 0v11q-26-18-52 0zM6 44q26-18 52 0v10q-26-18-52 0z',
 fanout:'M7 9h50v46H7zM15 18h12v12H15zM36 18h12v12H36zM20 30v14H9m33-14v14h13M32 11v40',
 via:'M8 9h48v48H8zM19 9v48m7-48v48m12-48v48m7-48v48',
 bridge:'M7 12h20v17H7zM37 12h20v17H37zM23 35h18v8H23zM16 29v23m32-23v23M6 52h52M25 29v6m14-6v6',
 routing:'M7 12h24v9H7zM31 17h11v28h15v9H31V29H17v15H7',
 chiplet:'M5 17h20v30H5zM39 17h20v30H39zM25 25h14m-5-4 5 4-5 4M39 39H25m5-4-5 4 5 4',
 memory:'M8 19h19v28H8zM36 11h21v8H36zM36 25h21v8H36zM36 39h21v8H36zM5 56h54',
 thermal:'M11 30h42v9H11zM11 45h42v9H11zM18 24V7m-4 4 4-4 4 4M32 24V7m-4 4 4-4 4 4M46 24V7m-4 4 4-4 4 4',
 pdn:'M7 15h15v34H7zM42 15h15v34H42zM22 22h20M22 43h20M32 22v7m-6 0h12m-12 7h12m-6 0v7',
 signal:'M6 18h18l13 20h21M6 27h13l13 20h26M5 56h54',
 shield:'M9 55V12h46v43M19 35h26v17H19zM5 58h54M9 23H4m51 0h5',
 rlc:'M3 32h7l4-10 6 20 6-20 4 10h4q4-17 8 0h4m0-11v22m7-22v22m0-11h8',
 capacitor:'M5 32h19M24 15v34m14-34v34M38 32h21',
 cooling:'M11 10h42v46H11zM11 20h31v7H21v10h22v7H11M4 20h7m42 24h7',
 sealed:'M10 53V12h44v41M19 37h26v16H19zM5 56h54M18 19h11v6H18z',
 sinter:'M7 10h50v7H7zM7 49h50v7H7zM11 24h9v8h-9zM26 26h9v8h-9zM42 23h9v8h-9zM18 35h9v9h-9zM35 36h9v9h-9z',
 ceramic:'M8 13h48v9H8zM8 22h48v20H8zM8 42h48v9H8zM18 30h28',
 cycle:'M8 9v48h48M14 44h8V19h12v25h12V19h9',
 moisture:'M8 33h48v23H8zM16 7l-5 10a6 6 0 0 0 12 0zM45 7l-5 10a6 6 0 0 0 12 0zM21 47l8-5 7 6 8-3',
 acoustic:'M8 47h27v10H8zM15 7h14v12H15zM17 23l7 18 8-18M39 53V16m0 37h22M42 49h5V25h5v24h7',
 ct:'M5 25h9v14H5zM28 22h14v21H28zM52 13h7v39h-7zM14 31l38-18M14 33l38 19M25 50q16 11 25-4',
 waveguide:'M7 42h50v14H7zM7 29h50v13H7zM24 21h16v15H24z',
 grating:'M7 51h50M10 39h5v12h-5zM20 39h5v12h-5zM30 39h5v12h-5zM40 39h17v12M18 7l17 26m-7-3 7 3v-8',
 taper:'M5 27h17v10H5zM25 31l31-17v36L25 33z',
 align:'M5 27h22v10H5zM39 22h18v20H39zM21 14h15m-4-4 4 4-4 4M33 41v17m-4-4 4 4 4-4',
 split:'M5 32h17q10 0 14-13h23M22 32q10 0 14 13h23',
 mzi:'M4 32h10l12-16h16l10 16h9M14 32l12 16h16l10-16M27 10h15',
 ring:'M6 53h52M16 29a16 16 0 1 0 32 0a16 16 0 1 0-32 0',
 detector:'M6 45h52M22 31h22v14H22zM26 24v7m14-7v7M9 8l15 15m-7-1 7 1-1-7',
 heater:'M5 49h54M9 17h8v15h9V17h9v15h9V17h10M22 36v7m19-7v7',
 junction:'M7 28h50v21H7zM32 28v21M17 28V12h11m9 0h12v16M24 9v6m-3-3h6m15 0h8',
 laserchip:'M7 43h50v12H7zM18 25h28v18H18zM24 16h16v9H24zM5 32h9m36 0h9',
 awg:'M3 32h11l8-14v28l-8-14M61 32H50l-8-14v28l8-14M22 21q10-23 20 0M22 29q10-16 20 0M22 37q10-9 20 0',
 mesh:'M8 8h48v48H8zM8 24h48M8 40h48M24 8v48M40 8v48M20 20h8v8h-8zM36 36h8v8h-8z',
 coherent:'M3 17h19M3 47h19M22 10h21v44H22zM43 17h16M43 27h16M43 37h16M43 47h16',
 array:'M5 14h30m-30 12h30M5 38h30m-30 12h30M38 14l20-8m-20 20 20-8m-20 20 20-8m-20 20 20-8',
 lidar:'M4 25h15v16H4zM29 19h17v28H29zM19 32h10m17-7h9v13h-9M58 9v45M37 47v10H15',
 sensor:'M5 52h54M17 33a15 15 0 1 0 30 0a15 15 0 1 0-30 0M22 6v10m10-13v10m10-7v10',
 spectrum:'M8 9v47h49M16 51V36m8 15V25m8 26V15m8 36V25m8 26V36',
 quantum:'M4 32h14M18 21h22v22H18zM40 25l17-14M40 39l17 14M52 6h9v10h-9zM52 48h9v10h-9z',
 feedback:'M7 12h18v15H7zM39 12h18v15H39zM25 19h14M48 27v22H17V27M27 43h11v12H27z',
 reroute:'M5 32l20-20h16l18 20M5 32l20 20h16l18-20M28 7l9 10m-9 0 9-10',
 pdk:'M6 8h21v21H6zM37 8h21v21H37zM6 39h21v21H6zM37 39h21v21H37zM27 18h10M17 29v10M48 29v10M27 49h10',
 cpo:'M21 22h23v23H21zM4 6h12v14H4zM48 6h12v14H48zM4 46h12v14H4zM48 46h12v14H48zM16 16l7 8m19 0 7-8M16 49l7-6m19 0 7 6',
 interlock:'M5 23h17v22H5zM22 34h15M39 12h19v41H39zM30 25v18M29 25V9h20v3'
};
const groups={stack:'stack soic foveros',pillar:'pillar',bond:'bond directbond',wafer:'waferbond',transfer:'diebond temporary transferlaser',grind:'grind',laser:'laserdice',dice:'plasmadice',pick:'pick',underfill:'underfill adhesive',warp:'warpage fatigue thermomech stressphase',fanout:'fanout panel sip',via:'viaetch viafill viareveal glassvia',bridge:'bridge emib',routing:'rdl embed interposer organic glasscore build-up package',chiplet:'chiplet opticalio codesign',memory:'hbm cowos',thermal:'thermal tim doublecool',pdn:'pdn converter',signal:'signal directional',shield:'shield emc',rlc:'rlc',capacitor:'decap',cooling:'cooling',sealed:'hermetic vacuum',sinter:'sinter',ceramic:'ceramic',cycle:'cycling',moisture:'moisture',acoustic:'acoustic',ct:'ct',waveguide:'soiwave sinwave swg ln',grating:'grating',taper:'edge',align:'activealign passivealign opticalprobe',split:'polarization mmi',mzi:'mzi isipp',ring:'ring ringfilter',detector:'detector avalanche',heater:'heater',junction:'junction',laserchip:'iiivlaser qdlaser external soa',awg:'awg',mesh:'switch mesh',coherent:'coherent',array:'opa',lidar:'lidar',sensor:'biosensor midinfrared',spectrum:'comb',quantum:'quantum',feedback:'feedback',reroute:'reroute',pdk:'pdk',cpo:'cpo',interlock:'interlock'};
const familyToGlyph=Object.fromEntries(Object.entries(groups).flatMap(([k,v])=>v.split(' ').map(f=>[f,k])));
export const packagingIconFamilies=Object.freeze(Object.keys(glyphs));
export function renderPackagingIcon(courseId,{en=false}={}){
 const s=PACKAGING_SUBJECTS[courseId],g=s&&familyToGlyph[s.family];if(!s||!g)return '';
 const title=en?s.titleEn:s.title,desc=en?'Original mechanism-family pictogram; related courses share a symbol.':'原創工法類型圖示；相近課程共用類型符號。';
 return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 88 104" class="project-icon" role="img" aria-label="${e(title+' · '+courseId+' · '+desc)}" data-project-icon="${e(courseId)}" data-subject-art="${e(courseId)}" data-icon-family="${e(g)}"><title>${e(title)}</title><desc>${e(desc)}</desc><rect x="4" y="4" width="80" height="82" rx="15" fill="#edf3e6" stroke="#91a78b" stroke-width="1.4"/><g transform="translate(12 12)" data-icon-geometry="${e(g)}" fill="none" stroke="#315344" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="${glyphs[g]}"/></g><text x="44" y="99" text-anchor="middle" font-family="ui-monospace,monospace" font-size="${courseId.length>8?6:9}" fill="#244a36">${e(courseId.toUpperCase())}</text></svg>`;
}
