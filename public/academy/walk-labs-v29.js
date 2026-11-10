/* Original software-laboratory teaching models. No production system is accessed. */
import {calculateLab as previousCalculate,restoreLabRun as previousRestore,mountLab as previousMount} from './walk-labs-v28.js';
const input=(id,title,titleEn,value,min,max,step=1)=>({id,title,titleEn,value,min,max,step});
const exp=(id,title,titleEn,inputs,unit,calculate,limit,validate)=>({id,title,titleEn,inputs,unit,calculate,limit,validate});
export const LAB_EXPERIMENTS_V29=Object.freeze({
 'software-build-match':exp('software-build-match','重建產物逐檔比對','Rebuilt artifact comparison',[
  input('files','逐位元比對檔案數','Files compared byte for byte',128,1,1000000),input('different','內容不同檔案數','Files with different contents',3,0,1000000)],'%',v=>100*(v.files-v.different)/v.files,
  ['比對一致率=(總檔案−不同檔案)/總檔案×100%。清單先需檢查缺檔、多檔及路徑；99% 不能當作可重現建置通過。雜湊相同不是供應鏈可信的證明。','Match rate=(files−different)/files×100%. First check missing files, extra files and paths. A 99% match is not a reproducible-build pass. Matching hashes do not establish supply-chain trust.'],v=>v.different<=v.files),
 'software-build-dag':exp('software-build-dag','平行建置的關鍵路徑','Critical path of a parallel build',[
  input('compile','編譯分支耗時 (s)','Compilation branch (s)',42,0,100000),input('assets','資源分支耗時 (s)','Asset branch (s)',25,0,100000),input('link','合併與連結 (s)','Merge and link (s)',8,0,100000),input('tests','末端測試 (s)','Final tests (s)',36,0,100000)],'s',v=>Math.max(v.compile,v.assets)+v.link+v.tests,
  ['T=max(Tcompile,Tassets)+Tlink+Ttests；兩條分支同時啟動且資源互不競爭。不是把全部耗時相加，也不是所有工作可同時執行。實際排程、I/O及快取另測。','T=max(Tcompile,Tassets)+Tlink+Ttests assumes simultaneous independent branches, followed by link and tests. Neither summing every duration nor running every job simultaneously describes this DAG. Measure scheduling, I/O and cache effects separately.']),
 'software-transfer-invariant':exp('software-transfer-invariant','交易前後資產守恆','Conservation across a transaction',[
  input('beforeA','交易前 A (整數分)','A before (integer cents)',10000,0,1e9),input('beforeB','交易前 B (整數分)','B before (integer cents)',5000,0,1e9),input('afterA','交易後 A (整數分)','A after (integer cents)',7000,0,1e9),input('afterB','交易後 B (整數分)','B after (integer cents)',8000,0,1e9)],'cents',v=>v.afterA+v.afterB-v.beforeA-v.beforeB,
  ['Δ=(Aafter+Bafter)−(Abefore+Bbefore)；這個封閉轉帳模型應為0。使用整數分避免小數貨幣誤差；Δ=0只通過一項不變量，仍需檢查重複轉帳、隔離層級與崩潰原子性。','Δ=(Aafter+Bafter)−(Abefore+Bbefore) must be zero in this closed transfer model. Integer cents avoid floating currency rounding. Zero passes one invariant; duplicate transfers, isolation and crash atomicity remain separate checks.']),
 'software-ci-matrix':exp('software-ci-matrix','跨平台 CI 測試矩陣','Cross-platform CI test matrix',[
  input('systems','作業系統種類','Operating systems',3,1,100),input('runtimes','執行環境版本','Runtime versions',3,1,100),input('databases','資料庫版本','Database versions',2,1,100),input('excluded','明列排除組合數','Explicitly excluded combinations',2,0,1000000)],'jobs',v=>v.systems*v.runtimes*v.databases-v.excluded,
  ['工作數=OS×runtime×database−排除組合。假設各排除組合互異且屬於原笛卡兒積；需逐列檢查，不可重複扣除。工作數不等於涵蓋的行為數或正確性證明。','Jobs=OS×runtime×database−excluded combinations. Exclusions must be distinct members of the Cartesian product; check the rows, rather than subtracting duplicates. Job count is not behavioral coverage or proof of correctness.'],v=>v.excluded<=v.systems*v.runtimes*v.databases),
 'software-canary-delta':exp('software-canary-delta','金絲雀與基準錯誤率差','Canary minus baseline error rate',[
  input('canaryRequests','金絲雀請求數','Canary requests',1000,1,1e9),input('canaryErrors','金絲雀失敗數','Canary failures',8,0,1e9),input('baseRequests','基準請求數','Baseline requests',1000,1,1e9),input('baseErrors','基準失敗數','Baseline failures',2,0,1e9)],'percentage points',v=>100*(v.canaryErrors/v.canaryRequests-v.baseErrors/v.baseRequests),
  ['差值=100×(Ec/Nc−Eb/Nb)，單位百分點，正值表示此樣本的金絲雀錯誤率較高。須檢查共同時間窗、流量組成與樣本不確定性；單一差值不是統計顯著性或因果結論。','Difference=100×(Ec/Nc−Eb/Nb), in percentage points. Positive means the observed canary rate is higher. Check common windows, traffic mix and sampling uncertainty. This number alone is neither significance nor causality.'],v=>v.canaryErrors<=v.canaryRequests&&v.baseErrors<=v.baseRequests),
 'software-error-budget':exp('software-error-budget','請求型 SLO 剩餘錯誤預算','Remaining request-based SLO error budget',[
  input('requests','共同窗口合格請求數','Eligible requests in the window',100000,1,1e9),input('slo','成功率目標 (千分數)','Success target (per thousand)',999,0,1000),input('errors','已發生不合格請求數','Observed bad requests',45,0,1e9)],'requests',v=>v.requests*(1000-v.slo)/1000-v.errors,
  ['剩餘預算=N×(1000−SLO千分數)/1000−E；負值表示預算超支。假設分母、排除規則及窗口一致。這是請求型預算，不可直接換成停機分鐘；滾動窗口仍會改變。','Remaining budget=N×(1000−SLO per thousand)/1000−E. Negative means overspend. Denominator, exclusions and window must agree. This request-based budget cannot be directly converted into downtime minutes; a rolling window also changes.'],v=>v.errors<=v.requests)
});

export function calculateLab(id,values){
 const lab=LAB_EXPERIMENTS_V29[id];if(!lab)return previousCalculate(id,values);
 if(!values||typeof values!=='object'||Array.isArray(values))throw new RangeError('Missing inputs');
 const v={};for(const i of lab.inputs){const raw=values[i.id];if((typeof raw!=='number'&&typeof raw!=='string')||(typeof raw==='string'&&!raw.trim()))throw new RangeError(i.titleEn);v[i.id]=Number(raw);if(!Number.isFinite(v[i.id])||v[i.id]<i.min||v[i.id]>i.max||(i.step===1&&!Number.isInteger(v[i.id])))throw new RangeError(i.titleEn);}
 if(lab.validate&&!lab.validate(v))throw new RangeError('Incompatible inputs');
 const result=lab.calculate(v);if(!Number.isFinite(result))throw new RangeError('Non-finite result');return {result,unit:lab.unit};
}
export function restoreLabRun(id,raw){
 const lab=LAB_EXPERIMENTS_V29[id];if(!lab)return previousRestore(id,raw);
 if(!raw||raw.experimentId!==id||!raw.inputs||typeof raw.inputs!=='object'||Array.isArray(raw.inputs))return null;
 const inputs={};for(const i of lab.inputs){if(typeof raw.inputs[i.id]!=='number'||!Number.isFinite(raw.inputs[i.id]))return null;inputs[i.id]=raw.inputs[i.id];}
 try{return {experimentId:id,inputs,...calculateLab(id,inputs)};}catch{return null;}
}
export function mountLab(container,id,{language='en',onRun=()=>{},onInvalidate=()=>{},state={}}={}){
 const lab=LAB_EXPERIMENTS_V29[id];if(!lab)return previousMount(container,id,{language,onRun,state});
 const L=(a,b)=>language==='zh-TW'?a:b;state.inputs??={};state.lastRun=restoreLabRun(id,state.lastRun);
 container.className='walk-lab';container.innerHTML=`<h3>${L(lab.title,lab.titleEn)}</h3><p>${L('先記錄手算預測，再更動一個輸入；執行後將結果、條件及單位寫入本站紀錄。','Record a hand calculation, then change one input. Running saves the result, conditions and units in the station record.')}</p><form>${lab.inputs.map(i=>`<label>${L(i.title,i.titleEn)}<input name="${i.id}" type="number" min="${i.min}" max="${i.max}" step="${i.step}" required></label>`).join('')}<button type="submit">${L('執行與記錄','Run and record')} ▶</button><output aria-live="polite" data-private data-no-translate></output></form><p class="muted">${L(...lab.limit)}</p>`;
 const form=container.querySelector('form'),output=container.querySelector('output');
 const show=()=>{const r=state.lastRun;output.textContent=r?`${Number(r.result.toPrecision(9))} ${r.unit}`:'';};
 const invalidate=()=>{state.lastRun=null;onInvalidate(id);output.textContent=L('輸入已變更，請重新執行後再完成本站。','Inputs changed. Run again before completing this station.');};
 for(const i of lab.inputs){const control=form.elements.namedItem(i.id),saved=state.inputs[i.id];control.value=(typeof saved==='number'||typeof saved==='string'&&saved.length<100)?saved:i.value;state.inputs[i.id]=control.value;control.oninput=()=>{state.inputs[i.id]=control.value;invalidate();};}
 // Never treat an older saved result as evidence for different draft inputs.
 if(state.lastRun&&lab.inputs.some(i=>String(state.inputs[i.id]).trim()===''||Number(state.inputs[i.id])!==state.lastRun.inputs[i.id]))invalidate();else show();
 form.addEventListener('invalid',()=>{state.lastRun=null;onInvalidate(id);},true);
 form.onsubmit=e=>{e.preventDefault();if(!form.reportValidity()){state.lastRun=null;onInvalidate(id);return;}try{const values=Object.fromEntries(lab.inputs.map(i=>[i.id,form.elements.namedItem(i.id).value])),computed=calculateLab(id,values),inputs=Object.fromEntries(lab.inputs.map(i=>[i.id,Number(values[i.id])]));state.inputs={...inputs};state.lastRun={experimentId:id,inputs,...computed};show();onRun({id,values:inputs,...computed});}catch{state.lastRun=null;onInvalidate(id);output.textContent=L('數值無效或欄位不相容；未記錄完成。','Invalid or incompatible inputs. No completed run was recorded.');}};
}
