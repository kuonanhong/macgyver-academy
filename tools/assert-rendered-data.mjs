import assert from 'node:assert/strict';

// Compiler lessons legitimately discuss undefined behavior and floating-point
// lessons name NaN. Reject unresolved values at HTML value boundaries instead.
export function assertRenderedData(html, label) {
  assert.equal(typeof html, 'string');
  assert(!/\[object Object\]|>\s*(?:undefined|NaN)\s*<|\b(?:data-[\w-]+|href|src|value)=["'](?:undefined|NaN)["']/.test(html), `${label}: unresolved data value`);
  assert(!/href="#project\/(null|undefined)"/.test(html), `${label}: invalid related route`);
}
