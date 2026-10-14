import assert from 'node:assert/strict';
import fs from 'node:fs';
import {createRequire} from 'node:module';

// Use parsers already shipped with the project's declared build dependency.
// No browser, package download or generated CSS is required for this test.
const require = createRequire(import.meta.url);
const buildDependencies = createRequire(require.resolve('@tailwindcss/postcss'));
const postcss = buildDependencies('postcss');
const lightningcss = buildDependencies('lightningcss');
const file = new URL('../public/academy/style.css', import.meta.url);
const css = fs.readFileSync(file, 'utf8');
const parsed = postcss.parse(css, {from: file.pathname});
const native = lightningcss.transform({filename: 'style.css', code: Buffer.from(css), minify: false, errorRecovery: false});
assert.equal(native.warnings.length, 0, 'Native CSS parser warnings must be reviewed');

// The V4 font-URL tail must be caught as CSS, not merely by searching for :root.
const damagedPrefix = "500;600;700&family=Noto+Sans+TC:wght@400;500;600;700;800&display=swap');\n";
assert.throws(() => postcss.parse(damagedPrefix + ':root{--green:#235443}'), 'The historical malformed prefix must fail parsing');
const firstRule = parsed.nodes.find(node => node.type !== 'comment');
assert.equal(firstRule.type, 'rule');
assert.equal(firstRule.selector, ':root', 'Colour variables must belong to an actual parsed :root rule');

const roots = {};
for (const node of parsed.nodes) if (node.type === 'rule' && node.selector === ':root') {
  node.walkDecls(decl => { roots[decl.prop] = decl.value; });
}
for (const key of ['--ink', '--muted', '--line', '--bg', '--green', '--lime', '--orange', '--white', '--soft', '--mono']) {
  assert(roots[key], `Missing parsed theme variable ${key}`);
}
const compiled = postcss.parse(native.code.toString());
assert(compiled.nodes.some(node => node.type === 'rule' && node.selector === ':root' && node.nodes.some(decl => decl.prop === '--green')), 'Native compilation must retain theme variables');

function inMedia(rule, expression) {
  for (let node = rule.parent; node; node = node.parent) if (node.type === 'atrule' && node.name === 'media' && expression.test(node.params)) return true;
  return false;
}
function declarations(selectors, media = null) {
  const result = {};
  parsed.walkRules(rule => {
    if (!rule.selectors.some(selector => selectors.includes(selector))) return;
    if (media ? !inMedia(rule, media) : inMedia(rule, /./)) return;
    rule.walkDecls(decl => { result[decl.prop] = decl.value; });
  });
  return result;
}
const resolve = (value, variables = roots) => value.replace(/var\(\s*(--[\w-]+)\s*,\s*([^()]+)\)/g, (_, key, fallback) => variables[key] || fallback.trim());
const luminance = value => {
  const match = value.match(/^#([\da-f]{3}|[\da-f]{6})$/i);
  assert(match, `Contrast colour is a concrete sRGB value: ${value}`);
  const hex = match[1].length === 3 ? [...match[1]].map(c => c + c).join('') : match[1];
  const channels = [0, 2, 4].map(offset => parseInt(hex.slice(offset, offset + 2), 16) / 255).map(c => c <= .04045 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4);
  return channels[0] * .2126 + channels[1] * .7152 + channels[2] * .0722;
};
const ratio = (foreground, background) => {
  const values = [luminance(foreground), luminance(background)].sort((a, b) => b - a);
  return (values[0] + .05) / (values[1] + .05);
};
const contrasts = [];
for (const [label, selectors] of [
  ['Primary button', ['.button']],
  ['Learner assistance', ['.button', '.apprentice-assistance #assist']],
  ['Next action', ['.button', '.workshop-action-dock #complete']],
  ['Guide next action', ['.mentor-guide-actions button', '.mentor-guide-actions #mentorGuideNext']],
  ['Secondary button', ['.button', '.button.light']],
]) {
  const style = declarations(selectors);
  const background = resolve(style.background);
  const foreground = resolve(style.color);
  const contrast = ratio(foreground, background);
  assert(contrast >= 4.5, `${label}: normal text needs 4.5:1 contrast, got ${contrast.toFixed(2)}:1`);
  assert(parseFloat(style['min-height']) >= 44, `${label}: minimum 44px touch target`);
  contrasts.push(`${label} ${contrast.toFixed(2)}:1`);
  if (label !== 'Secondary button' && label !== 'Guide next action') {
    assert.match(style.background, /var\(--green,\s*#[\da-f]{6}\)/i, `${label}: explicit fallback avoids white-on-white if theme variables disappear`);
    assert(ratio(resolve(style.color, {}), resolve(style.background, {})) >= 4.5, `${label}: fallback colours remain readable`);
  }
}
assert(ratio(roots['--muted'], roots['--bg']) >= 4.5, 'Small secondary text must remain legible');
assert(ratio(roots['--guide-red'], '#fff') >= 3, 'Guide arrow must contrast with its white halo');

const dock = declarations(['.workshop-action-dock']);
assert.equal(dock.position, 'fixed', 'Next action must remain visible before and after scrolling to its DOM location');
assert.equal(dock.bottom, '0');
assert(dock['inset-inline-start'] && dock['inset-inline-end'], 'Dock uses logical insets for RTL');
assert(parseFloat(roots['--workshop-dock-clearance']) >= 180, 'Content needs clearance below the persistent dock');
assert(declarations(['.work-content'])['padding-block-end'].includes('--workshop-dock-clearance'));
assert.equal(declarations([':root'], /max-width:\s*700px/)['--workshop-sidebar-width'], '0px', 'Mobile dock spans the viewport');
assert(parseFloat(declarations(['.workshop-action-dock #complete'], /max-width:\s*700px/)['min-height']) >= 52);
assert.equal(declarations(['.workshop-action-dock .action-requirements'])['overflow-y'], 'auto', 'Long translated requirements stay accessible');
assert.equal(declarations(['[hidden]']).display, 'none', 'Hidden controls must not be exposed by .button display styles');

const arrow = declarations(['.mentor-guide-arrow']);
assert.equal(arrow.position, 'fixed');
assert.equal(arrow['pointer-events'], 'none', 'Arrow must not intercept clicks on the highlighted control');
assert.equal(arrow.transform, undefined, 'Arrow rotation is owned by guide positioning code');
assert(declarations(['.mentor-guide-target']).outline.includes('--guide-red'));
assert.equal(declarations(['.mentor-guide-arrow'], /prefers-reduced-motion:\s*reduce/).animation, 'none');
assert.equal(declarations(['.mentor-guide-target'], /forced-colors:\s*active/)['outline-color'], 'Highlight');
assert(declarations(['button:focus-visible']).outline.startsWith('3px solid'), 'Keyboard focus must be visibly outlined');
assert.equal(declarations(['.related-preview-grid']).display, 'grid', 'Related-preview markup uses its inner grid');
assert.equal(declarations(['.related-preview-grid'], /max-width:\s*700px/)['grid-template-columns'], 'minmax(0, 1fr)');

parsed.walkAtRules('import', rule => assert(!/https?:/i.test(rule.params), 'Offline CSS must not request remote stylesheets'));
parsed.walkDecls(decl => assert(!/url\(\s*['"]?(?:https?:)?\/\//i.test(decl.value), 'Offline CSS must not request remote assets'));
console.log(`CSS semantic PASS: PostCSS + native Lightning CSS parse; ${Object.keys(roots).length} theme variables; accessible controls, fallback colours, mobile/RTL dock, focus/guide semantics, no remote resources. ${contrasts.join('; ')}.`);
