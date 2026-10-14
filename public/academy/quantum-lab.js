/* Original, dependency-free ideal two-qubit learning model.
 * Basis order is |q0 q1>: 00,01,10,11. No QPU/cloud calls or noise claims. */
const e=v=>String(v??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const add=(a,b)=>[a[0]+b[0],a[1]+b[1]],mul=(a,b)=>[a[0]*b[0]-a[1]*b[1],a[0]*b[1]+a[1]*b[0]],conj=a=>[a[0],-a[1]],abs2=a=>a[0]**2+a[1]**2;
const zero=()=>[[1,0],[0,0],[0,0],[0,0]];
export function quantumState(operations=[]){
 if(!Array.isArray(operations)||operations.length>64)throw new RangeError('Use at most 64 ideal gates.');
 let state=zero();
 for(const op of operations){
  if(!op||!['H','X','Z','S','T','RY','CX','CZ','SWAP'].includes(op.gate))throw new TypeError('Unsupported ideal gate.');
  if(op.gate==='CX'||op.gate==='CZ'){
   const c=op.control??0,t=op.target??1;if(![0,1].includes(c)||![0,1].includes(t)||c===t)throw new RangeError('Distinct qubits required.');
   const cb=2>>c,tb=2>>t,out=state.map(()=>[0,0]);
   for(let i=0;i<4;i++){const active=!!(i&cb),j=op.gate==='CX'&&active?i^tb:i;out[j]=op.gate==='CZ'&&active&&(i&tb)?state[i].map(v=>-v):[...state[i]];}state=out;continue;
  }
  if(op.gate==='SWAP'){state=[state[0],state[2],state[1],state[3]];continue;}
  const q=op.target??0;if(![0,1].includes(q))throw new RangeError('Qubit must be 0 or 1.');
  let m;const s=Math.SQRT1_2;
  if(op.gate==='H')m=[[[s,0],[s,0]],[[s,0],[-s,0]]];
  if(op.gate==='X')m=[[[0,0],[1,0]],[[1,0],[0,0]]];
  if(op.gate==='Z')m=[[[1,0],[0,0]],[[0,0],[-1,0]]];
  if(op.gate==='S')m=[[[1,0],[0,0]],[[0,0],[0,1]]];
  if(op.gate==='T')m=[[[1,0],[0,0]],[[0,0],[s,s]]];
  if(op.gate==='RY'){const a=Number(op.angle);if(!Number.isFinite(a)||Math.abs(a)>4*Math.PI)throw new RangeError('Angle exceeds model range.');const c=Math.cos(a/2),r=Math.sin(a/2);m=[[[c,0],[-r,0]],[[r,0],[c,0]]];}
  const bit=2>>q,out=state.map(a=>[...a]);
  for(let i=0;i<4;i++)if(!(i&bit)){const j=i|bit;out[i]=add(mul(m[0][0],state[i]),mul(m[0][1],state[j]));out[j]=add(mul(m[1][0],state[i]),mul(m[1][1],state[j]));}state=out;
 }
 const probabilities=state.map(abs2),norm=probabilities.reduce((a,b)=>a+b,0);
 const [a,b,c,d]=state,ad=mul(a,d),bc=mul(b,c),det=[ad[0]-bc[0],ad[1]-bc[1]],concurrence=Math.min(1,2*Math.sqrt(abs2(det)));
 const r00=abs2(a)+abs2(b),r11=abs2(c)+abs2(d),r01=add(mul(a,conj(c)),mul(b,conj(d))),purity=r00*r00+r11*r11+2*abs2(r01);
 return {state,probabilities,norm,concurrence,purity};
}
// Explicit curriculum metadata selects this foundational ideal-gate model.
// Quantum-dot materials and post-quantum cryptography are not gate-model labs.
export function isQuantumCourse(course={}){return course.learningTrack==='quantum';}
export function quantumLabMarkup(course,zh=true){
 if(!isQuantumCourse(course))return '';
 const comparison=course.learningSubdiscipline==='quantum-annealing'?(zh?'本課研究退火／Ising 能量模型；以下用閘模型作比較，不表示該退火機可直接執行 H、CX 等閘。':'This course concerns annealing/Ising energy models. The gate model below is a comparison and does not imply an annealer directly runs H or CX gates.'):course.learningSubdiscipline==='quantum-topological'?(zh?'以下驗證數學模型，不能證實本課研究裝置已具拓樸保護或容錯能力。':'The mathematics below does not establish topological protection or fault tolerance of a research device.') : '';
 return `<section class="lesson-card quantum-lab" id="quantumLab"><div class="eyebrow">IDEAL STATEVECTOR / CPU</div><h3>${zh?'兩量子位：親手建立疊加、相位與糾纏':'Two qubits: build superposition, phase and entanglement'}</h3><p>${zh?'以 |q0 q1⟩ 的順序顯示 00、01、10、11；矩陣作用於四個複數振幅。這是理想閘模擬，不包含硬體校準、退相干或實際 QPU 量測。':'Basis order is |q0 q1⟩: 00, 01, 10, 11. Matrices act on four complex amplitudes. This ideal-gate model excludes calibration, decoherence and physical QPU measurement.'}</p>${comparison?`<p class="notice">${e(comparison)}</p>`:''}<div class="quantum-controls"><label>${zh?'目標量子位':'Target qubit'} <select id="quantumTarget"><option value="0">q0</option><option value="1">q1</option></select></label>${['H','X','Z','S','T'].map(g=>`<button class="button light" type="button" data-quantum-gate="${g}">${g}</button>`).join('')}<button class="button light" type="button" data-quantum-gate="CX">CX q0→q1</button><button class="button light" type="button" data-quantum-gate="CZ">CZ</button><button class="button light" type="button" data-quantum-gate="SWAP">SWAP</button></div><div class="quantum-controls"><label>${zh?'RY 旋轉角 θ':'RY rotation θ'} <input id="quantumAngle" type="number" min="-360" max="360" step="15" value="90"> °</label><button class="button light" type="button" data-quantum-gate="RY">RY(θ)</button><button class="button" type="button" id="quantumBell">${zh?'示範 Bell 態':'Bell-state example'}</button><button class="button light" type="button" id="quantumUndo">${zh?'撤回一閘':'Undo gate'}</button><button class="button light" type="button" id="quantumReset">|00⟩ ${zh?'重設':'Reset'}</button></div><div id="quantumResult" aria-live="polite"></div><p class="notice">${zh?'先 H(q0) 再 CX(q0→q1)，00 與 11 各為 50%。再加 Z(q0)：機率不變，但相對相位改變；再以 H 閘干涉即可探究相位如何影響不同基底的結果。糾纏度指標僅適用於本純態模型，不能由單一 Z 基底直方圖判定。':'Apply H(q0), then CX(q0→q1): 00 and 11 each have 50% probability. Add Z(q0): probabilities remain but relative phase changes. Interference with H gates explores a different measurement basis. The entanglement metric applies only to this pure-state model; a single Z-basis histogram does not establish entanglement.'}</p><a href="https://quantum.cloud.ibm.com/learning/en/courses/use-a-qc-today/quantum-mechanics-basics" target="_blank" rel="noopener noreferrer">IBM Quantum · ${zh?'原理延伸閱讀':'Principle reference'} ↗</a></section>`;
}
export function bindQuantumLab(course,zh=true){
 if(typeof document==='undefined'||!isQuantumCourse(course))return;
 const root=document.querySelector('#quantumLab');if(!root?.querySelectorAll)return;let operations=[];
 const update=message=>{const result=quantumState(operations),fmt=v=>(Math.abs(v)<1e-10?0:v).toFixed(4),node=root.querySelector('#quantumResult');if(!node)return;node.innerHTML=`${message?`<p role="status">${e(message)}</p>`:''}<p><strong>${zh?'閘序列':'Gate sequence'}:</strong> ${operations.length?operations.map(o=>e(o.gate+(o.gate==='CX'?'(0→1)':o.gate==='CZ'||o.gate==='SWAP'?'':`(q${o.target}${o.gate==='RY'?','+(o.angle*180/Math.PI).toFixed(0)+'°':''})`))).join(' → '):'|00⟩'}</p><div class="quantum-table"><table><thead><tr><th>${zh?'基底':'Basis'}</th><th>${zh?'振幅：實部 + i 虛部':'Amplitude: real + i imaginary'}</th><th>${zh?'理想機率':'Ideal probability'}</th></tr></thead><tbody>${result.state.map((v,i)=>`<tr><td>|${i.toString(2).padStart(2,'0')}⟩</td><td>${fmt(v[0])} ${v[1]<0?'−':'+'} i ${fmt(Math.abs(v[1]))}</td><td>${(100*result.probabilities[i]).toFixed(2)}%</td></tr>`).join('')}</tbody></table></div><p>Σ|α|² = ${fmt(result.norm)} · Tr(ρq0²) = ${fmt(result.purity)} · C = ${fmt(result.concurrence)}</p>`;};
 root.querySelectorAll('[data-quantum-gate]').forEach(button=>button.onclick=()=>{if(operations.length>=64){update(zh?'本示意最多 64 閘，請撤回或重設。':'This model accepts 64 gates. Undo or reset.');return;}const gate=button.dataset.quantumGate,target=Number(root.querySelector('#quantumTarget').value);const op=gate==='CX'||gate==='CZ'?{gate,control:0,target:1}:gate==='SWAP'?{gate}:{gate,target};if(gate==='RY'){const value=Number(root.querySelector('#quantumAngle').value);if(!Number.isFinite(value)||value < -360||value>360){update(zh?'請輸入 −360 至 360 度。':'Enter −360 to 360 degrees.');return;}op.angle=value*Math.PI/180;}operations.push(op);update();});
 const bind=(selector,fn)=>{const el=root.querySelector(selector);if(el)el.onclick=fn;};bind('#quantumBell',()=>{operations=[{gate:'H',target:0},{gate:'CX',control:0,target:1}];update();});bind('#quantumUndo',()=>{operations.pop();update();});bind('#quantumReset',()=>{operations=[];update();});update();
}
