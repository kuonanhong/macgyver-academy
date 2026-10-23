import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {calculateEnvironmentExpression as calc,environmentLabMarkup} from '../../public/academy/environment-lab-v17.js';
test('operator precedence, unary signs and scientific notation',()=>{
  assert.equal(calc('2+3*4'),14);assert.equal(calc('-2**2'),-4);assert.equal(calc('2**3**2'),512);
  assert.equal(calc('2**-2'),.25);assert.equal(calc('8*(20//2.5)'),64);assert.equal(calc('sqrt(9)+ceil(1.2)'),5);assert.equal(calc('1e-3*20'),.02);
});
test('invalid values and program text never execute',()=>{
  for(const value of ['process.exit()','1/0','2;alert(1)','x=3','1<2','min.constructor(2)','sqrt(-1)'])assert.throws(()=>calc(value));
});
test('all authored environment arithmetic runs in the actual browser interpreter',()=>{
  const root=path.dirname(fileURLToPath(import.meta.url));let count=0;
  for(const name of fs.readdirSync(path.join(root,'inputs')).filter(n=>/^b\d+\.json$/.test(n))){
    const c=JSON.parse(fs.readFileSync(path.join(root,'inputs',name)));for(const m of c.modelChecks){const actual=calc(m.expression),tolerance=Math.max(m.absoluteTolerance||1e-5,Math.abs(m.expected)*(m.relativeTolerance||1e-5));assert.ok(Math.abs(actual-m.expected)<=tolerance,`${c.id}: ${m.expression}: ${actual} != ${m.expected}`);count++;}
  }
  assert.ok(count>=1000,`Expected all 100 courses, only ${count} examples were present`);
});
test('new lesson markup escapes authored content and omits unrelated steps',()=>{
  assert.equal(environmentLabMarkup({},true),'');
  const markup=environmentLabMarkup({environmentExample:{expression:'<img src=x>',unit:'kg'},observation:'<script>x</script>'},true);
  assert.ok(!markup.includes('<script>'));assert.ok(markup.includes('&lt;img'));
});
