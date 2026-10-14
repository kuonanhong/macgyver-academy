/* Original functional relationships drawn from course-authored components.
 * Not a vendor drawing, physical CAD, plant layout or as-built document. */
const e=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const identityHash=v=>{let n=2166136261;for(const c of String(v)){n^=c.codePointAt(0);n=Math.imul(n,16777619);}return n>>>0;};
const colors=['#315f62','#527eaa','#b47a34','#754c86','#487d55'];
function wrapLabel(value){
 const text=String(value??''),limit=/[^\x00-\x7f]/.test(text)?13:24,words=text.includes(' ')?text.split(/\s+/):[...text],lines=[];let line='';
 for(const word of words){const next=line+(line&&text.includes(' ')?' ':'')+word;if(next.length>limit&&line){lines.push(line);line=word;}else line=next;}if(line)lines.push(line);return lines;
}
export function worldVisualFamily(course={}){return course.architectureFamily||'';}
function motif(family){
 if(/qpu|quantum/.test(family))return '<circle cx="0" cy="0" r="25"/><ellipse cx="0" cy="0" rx="36" ry="11" transform="rotate(35)"/><ellipse cx="0" cy="0" rx="36" ry="11" transform="rotate(-35)"/><circle cx="0" cy="0" r="4" fill="currentColor"/>';
 if(family==='fusion')return '<ellipse rx="34" ry="23"/><ellipse rx="22" ry="13"/><path d="M-34-5v10M34-5v10M-12-22v9M12-22v9M-12 13v9M12 13v9"/>';
 if(family==='wind')return '<circle r="5"/><path d="M0 5v36M0-5L8-35-4-36Z M4 2L33 13 30 24Z M-4 2L-29 21-33 11Z"/>';
 if(family==='hydro')return '<path d="M-34-26H34L15 18H-6V-26M-34-4h18M-34 13h18M-28 31q7-9 14 0t14 0 14 0 14 0"/><circle cx="9" cy="18" r="12"/><path d="M9 6V30M-3 18H21"/>';
 if(family==='geothermal')return '<path d="M-36-8H36M-21-30V27H21V-30M-13 27V-19H13V27M-30 35q10-8 20 0t20 0M-30-24H-8M8-24H30"/>';
 if(family==='oil')return '<path d="M-34-3H34M-22-3V32M22-3V32M-14-3V-32H14V-3M-14-32L14-3M14-32L-14-3M-34 33q11-7 22 0t22 0"/>';
 if(family==='mining')return '<path d="M-36-12L-15-30 4-14 23-32 36-8M-36-12V27H36V-8M-25-3H24M-25 9H24M-25 21H24M-3-3V21"/>';
 if(family==='ai')return '<rect x="-31" y="-31" width="62" height="62" rx="6"/><path d="M-17-31V31M0-31V31M17-31V31M-31-17H31M-31 0H31M-31 17H31"/>';
 if(family==='server')return '<rect x="-27" y="-33" width="54" height="66" rx="3"/><path d="M-27-11H27M-27 11H27M-14-23H10M-14 0H10M-14 23H10"/><circle cx="18" cy="-23" r="2"/><circle cx="18" cy="0" r="2"/><circle cx="18" cy="23" r="2"/>';
 return '<path d="M-35-23H-10V23H-35ZM10-23H35V23H10ZM-10-12H10M-10 12H10M-25-34V-23M25 23V34"/><path d="M-24-12q12 12 0 24M24-12q-12 12 0 24"/>';
}
function componentMotif(name,family){
 const n=String(name).toLowerCase();
 if(/monitor|diagnostic|readout|measurement|meter/.test(n))return '<rect x="-32" y="-25" width="64" height="43" rx="3"/><path d="M-25 0h11l7-13 13 23 8-10h11M0 18v12M-16 30h32"/>';
 if(/control|scheduler|decoder|orchestrat/.test(n))return motif('server');
 if(/microwave|pulse|laser/.test(n))return '<path d="M-36 0q9-25 18 0t18 0 18 0 18 0M-27-27v9m18-13v13m18-13v13m18-9v9"/>';
 if(/memory|buffer/.test(n))return '<rect x="-26" y="-23" width="52" height="46"/><path d="M-18-23v-10m12 10v-10m12 10v-10m12 10v-10M-18 23v10m12-10v10m12-10v10m12-10v10M-38-12h12m-12 12h12m-12 12h12M26-12h12m-12 12h12m-12 12h12"/>';
 if(/fabric|interconnect|array\/cable|optical path/.test(n))return '<circle cx="0" cy="0" r="6"/><circle cx="-28" cy="-20" r="6"/><circle cx="28" cy="-20" r="6"/><circle cx="-28" cy="20" r="6"/><circle cx="28" cy="20" r="6"/><path d="M-22-16L-6-4M6-4L22-16M-22 16L-6 4M6 4L22 16"/>';
 if(/cryogen|cool|heat exhaust|condens|reinjection/.test(n))return '<path d="M-32-20H-15V20H0V-20H15V20H32M-32-30H32M-32 30H32"/><path d="M-24-36l-4 5 4 5M24 25l4 5-4 5"/>';
 if(/turbine|drivetrain|generator/.test(n))return '<circle r="26"/><circle r="7"/><path d="M0-7V-26M7 0H26M0 7V26M-7 0H-26M-5-5L-19-19M5-5L19-19M5 5L19 19M-5 5L-19 19M26 0H38"/>';
 if(/rotor blade/.test(n))return motif('wind');
 if(/support|mooring|civil work/.test(n))return '<path d="M-26 28L0-29 26 28M-16 7H16M-24 25H24M-36 33q9-6 18 0t18 0 18 0 18 0"/>';
 if(/reservoir|tailwater|orebody/.test(n))return '<path d="M-36-21H36V29H-36ZM-35-6q9-6 18 0t18 0 18 0 18 0M-35 8q9-6 18 0t18 0 18 0 18 0"/><path d="M-24-30L-14-21M6-30L15-21M22 16v9M-20 16v9"/>';
 if(/well|waterway|feedwater/.test(n))return '<path d="M-32-24H-15V25H15V-24H32M-24-32h16m16 0h16M-24 33H24M-9-24v38H9V-24"/>';
 if(/heat transfer|heat exchang|steam/.test(n))return '<path d="M-35-23H-10V23H-35ZM10-23H35V23H10ZM-10-12H10M-10 12H10"/><path d="M-24-12q12 12 0 24M24-12q-12 12 0 24"/>';
 if(/heat source|vessel/.test(n))return '<rect x="-23" y="-31" width="46" height="62" rx="15"/><path d="M-12-23v42M0-23v42M12-23v42M-23-9h-13M23 9h13"/>';
 if(/material handling|storage\/transfer/.test(n))return '<path d="M-36 12H30M-30 20H30M-22 12v16M22 12v16M-26 11l6-18h15l5 18M5 11L10-9h16l7 20"/>';
 if(/tailings|water\//.test(n))return '<path d="M-35-20H35L25 27H-25ZM-30-4q10-7 20 0t20 0 20 0M-27 11q9-6 18 0t18 0 18 0"/>';
 if(/separation|liberation/.test(n))return '<path d="M-34-28H34L15 8H-15ZM-15 8v18H15V8M0-28V8M-27-18h4m13 0h4m13 0h4m13 0h4"/>';
 if(/recovered|reconstruction|image input|classifier|convolution|residual|pooling|attention|hidden|tensor|compute/.test(n))return motif(family==='server'?'server':'ai');
 if(/conversion|process platform/.test(n))return '<rect x="-32" y="-23" width="64" height="46" rx="4"/><path d="M-23 4l8-17 10 27 10-27 10 17M-39 0h7M32 0h7"/>';
 return motif(family);
}
export function hasWorldVisual(course={}){return !!course.architectureFamily&&Array.isArray(course.architectureNodes)&&course.architectureNodes.length>=3;}
export function renderWorldIcon(course,{en=false}={}){if(!hasWorldVisual(course))return '';return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 88 104" class="project-icon" data-project-icon="${e(course.id)}" role="img" aria-label="${e(en?course.titleEn:course.title)}"><rect x="5" y="5" width="78" height="78" rx="18" fill="#eaf0ef"/><g transform="translate(44 44) scale(.85)" fill="none" stroke="#315f62" stroke-width="2.3" stroke-linejoin="round">${motif(course.architectureFamily)}</g>${Array.from({length:20},(_,i)=>`<rect x="${7+i*3.8}" y="${81-((identityHash(course.id)>>>i)&1)*3}" width="2" height="${2+((identityHash(course.id)>>>i)&1)*3}" fill="#527eaa"/>`).join('')}<text x="44" y="98" text-anchor="middle" font-size="7" fill="#315f62">${e(course.architectureFamily.toUpperCase())}</text></svg>`;}
export function renderWorldVisual(course,{zh=true,focus=-1}={}){
 if(!hasWorldVisual(course))return '';
 const nodes=course.architectureNodes.slice(0,5),positions=[[112,90],[300,90],[488,90],[200,264],[400,264]],edges=Array.isArray(course.architectureEdges)?course.architectureEdges:[[0,1],[1,2],[1,3],[3,4]];
 const label=n=>Array.isArray(n)?n[zh?0:1]:(zh?n.label:n.labelEn);
 const lines=edges.filter(v=>Array.isArray(v)&&v.length===2&&Number.isInteger(v[0])&&Number.isInteger(v[1])&&v[0]>=0&&v[1]>=0&&v[0]<nodes.length&&v[1]<nodes.length&&v[0]!==v[1]).map(([a,b])=>{const [x,y]=positions[a],[u,v]=positions[b],dx=u-x,dy=v-y,d=Math.hypot(dx,dy),cut=Math.min(79/Math.max(1e-9,Math.abs(dx)),57/Math.max(1e-9,Math.abs(dy))),sx=x+dx*(cut+4/d),sy=y+10+dy*(cut+4/d),tx=u-dx*(cut+7/d),ty=v+10-dy*(cut+7/d);return `<path d="M${sx.toFixed(1)} ${sy.toFixed(1)}L${tx.toFixed(1)} ${ty.toFixed(1)}" stroke="#819893" stroke-width="2" marker-end="url(#worldArrow-${e(course.id)})"/>`;}).join('');
 return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 600 370" class="world-project-visual" data-world-visual="${e(course.id)}" role="img" aria-label="${e(zh?course.title:course.titleEn)} · ${zh?'原創教學功能架構':'Original educational functional architecture'}"><defs><marker id="worldArrow-${e(course.id)}" markerWidth="7" markerHeight="7" refX="5" refY="3" orient="auto"><path d="M0 0L6 3L0 6" fill="none" stroke="#819893"/></marker></defs><rect width="600" height="370" rx="12" fill="#f2f5f3"/><text x="24" y="27" font-size="11" fill="#526c64">${e(course.architectureFamily.toUpperCase())} / ${e(course.id)}</text>${lines}${nodes.map((n,i)=>{const [x,y]=positions[i],active=focus===i,wrapped=wrapLabel(label(n)),size=Math.min(11,33/Math.max(1,wrapped.length));return `<g data-world-component="${i}"><title>${e(label(n))}</title><rect x="${x-79}" y="${y-47}" width="158" height="114" rx="10" fill="${active?'#fff1e8':'#fff'}" stroke="${active?'#c54932':colors[i]}" stroke-width="${active?3:1.5}"/><g transform="translate(${x} ${y-9}) scale(.65)" fill="none" stroke="${colors[i]}" stroke-width="2">${componentMotif(Array.isArray(n)?n[1]:n.labelEn||label(n),course.architectureFamily)}</g><text x="${x}" y="${y+35}" text-anchor="middle" font-size="${size}" fill="#253d36">${wrapped.map((line,j)=>`<tspan x="${x}" dy="${j?size+1:0}">${e(line)}</tspan>`).join('')}</text></g>`;}).join('')}<text x="24" y="351" font-size="10" fill="#526c64">${zh?'功能關係教學示意 · 非比例尺 · 非施工／設備運轉圖':'Educational functional relationships · Not to scale · Not a construction/operating drawing'}</text></svg>`;
}
