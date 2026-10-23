/* A small arithmetic interpreter: no eval, network or dynamic JavaScript. */
export function calculateEnvironmentExpression(input){
  if(typeof input!=='string'||input.length>500)throw Error('Expression is too long');
  const tokens=input.match(/(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?|[A-Za-z_][A-Za-z_0-9]*|\*\*|\/\/|[+*/(),-]/g)||[];
  if(tokens.join('')!==input.replace(/\s/g,''))throw Error('Use numbers, arithmetic and supported functions only');
  let at=0,depth=0;
  const fn={sqrt:Math.sqrt,log:Math.log,log10:Math.log10,exp:Math.exp,abs:Math.abs,min:Math.min,max:Math.max,ceil:Math.ceil,floor:Math.floor,round:(n,d=0)=>Math.round(n*10**d)/10**d};
  function atom(){if(++depth>40)throw Error('Expression nesting is too deep');let t=tokens[at++],v;
    if(t==='('){v=sum();if(tokens[at++]!==')')throw Error('Missing closing parenthesis');}
    else if(t==='pi'||t==='e')v=t==='pi'?Math.PI:Math.E;
    else if(Object.hasOwn(fn,t)){if(tokens[at++]!=='(')throw Error('Function needs parentheses');const args=[sum()];while(tokens[at]===','){at++;args.push(sum());}if(tokens[at++]!==')'||args.length>12)throw Error('Invalid function arguments');v=fn[t](...args);}
    else if(t!==undefined&&/^(?:\d|\.)/.test(t))v=Number(t);else throw Error('Expected a number');
    depth--;return v;}
  function power(){const v=atom();if(tokens[at]==='**'){at++;return v**unary();}return v;}
  function unary(){if(tokens[at]==='+'){at++;return unary();}if(tokens[at]==='-'){at++;return -unary();}return power();}
  function product(){let v=unary();while(['*','/','//'].includes(tokens[at])){const op=tokens[at++],r=unary();v=op==='*'?v*r:op==='/'?v/r:Math.floor(v/r);}return v;}
  function sum(){let v=product();while(['+','-'].includes(tokens[at])){const op=tokens[at++],r=product();v=op==='+'?v+r:v-r;}return v;}
  const result=sum();if(at!==tokens.length||!Number.isFinite(result))throw Error('Check the expression and denominator');return result;
}
const escape=value=>String(value??'').replace(/[&<>"']/g,ch=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[ch]));
export function environmentLabMarkup(step,zh){
  const m=step?.environmentExample;if(!m)return '';
  return `<section class="task-card environment-unit-lab" id="environmentUnitLab"><span class="task-label">V17 · ENGINEERING NOTEBOOK</span><h3>${zh?'本單元可操作算例':'Interactive example for this unit'}</h3><p>${escape(zh?step.observation:step.observationEn)}</p><form id="environmentCalcForm"><label for="environmentExpression">${zh?'算式（可修改數值，再計算）':'Expression (edit values, then calculate)'}</label><input id="environmentExpression" maxlength="500" value="${escape(m.expression)}" spellcheck="false" autocomplete="off"><div class="environment-calc-actions"><button class="button">${zh?'計算並比較':'Calculate and compare'}</button><button class="button light" type="button" id="environmentCalcReset">${zh?'還原基準':'Restore baseline'}</button><button class="button light" type="button" id="environmentCalcRecord">${zh?'寫入工程筆記':'Add to engineering notes'}</button></div></form><p id="environmentCalcResult" role="status"></p><p class="subtext">${zh?'支援 + − * / ** //、sqrt、log、log10、exp、abs、min、max、round、ceil、floor。輸出單位依本單元固定；修改算式時請自行核對量綱。記錄算例不會自動通過工序驗收。':'Supports + − * / ** //, sqrt, log, log10, exp, abs, min, max, round, ceil and floor. The unit is fixed for this example; verify dimensions when editing. Recording a calculation does not pass the workshop assessment.'}</p><p>${escape(zh?step.check:step.checkEn)}</p></section>`;
}
export function bindEnvironmentLab(step,zh,onRecord){
  const host=document.querySelector('#environmentUnitLab'),m=step?.environmentExample;if(!host||!m)return;
  const input=host.querySelector('#environmentExpression'),result=host.querySelector('#environmentCalcResult');let calculation=null;
  const run=()=>{try{const value=calculateEnvironmentExpression(input.value),baseline=calculateEnvironmentExpression(m.expression);calculation={expression:input.value,value};result.textContent=`${zh?'結果':'Result'}: ${Number(value.toPrecision(9))} ${m.unit} · ${zh?'基準':'Baseline'}: ${Number(baseline.toPrecision(9))} ${m.unit} · Δ ${Number((value-baseline).toPrecision(8))} ${m.unit}`;}catch{calculation=null;result.textContent=zh?'算式無法計算；請檢查括號、函數與分母。':'Cannot calculate. Check parentheses, functions and denominator.';}};
  host.querySelector('#environmentCalcForm').onsubmit=e=>{e.preventDefault();run();};
  host.querySelector('#environmentCalcReset').onclick=()=>{input.value=m.expression;run();};
  host.querySelector('#environmentCalcRecord').onclick=()=>{run();if(!calculation)return;onRecord?.(`${zh?'工程算例':'Engineering calculation'}: ${calculation.expression} = ${Number(calculation.value.toPrecision(9))} ${m.unit}`);result.textContent+=' · '+(zh?'已寫入筆記':'Added to notes');};run();
}
