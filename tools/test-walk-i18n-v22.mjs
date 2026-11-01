import assert from 'node:assert/strict';
import {
  UI_KEYS_V22, UI_LANGUAGES_V22, SUPPORTED_LANGUAGES_V22,
  resolveLanguage, uiText, languageChoices,
} from '../public/academy/walk-i18n-v22.js';

const expectedKeys = 'enter domains search role follow first overview interact approach guide task close next evidence choose complete saved exportRecord importRecord help fullscreen photos mentor move look zoom record journey home loading webglFallback modelScope language resetPosition pause resume narrate previous source machineTranslation untranslated controls objective notes saveNote'.split(' ');
assert.deepEqual([...UI_KEYS_V22], expectedKeys);
assert.equal(SUPPORTED_LANGUAGES_V22.length, 79);
assert.equal(new Set(SUPPORTED_LANGUAGES_V22).size, 79);
assert.equal(Object.keys(UI_LANGUAGES_V22).length, 20);
for (const code of ['zh-TW', 'en', 'zh-CN', 'ja', 'ko', 'es', 'fr', 'de', 'pt', 'it', 'ar', 'hi', 'vi', 'id', 'th', 'tr', 'ru', 'uk', 'pl', 'nl']) {
  const row = UI_LANGUAGES_V22[code];
  assert.ok(row, code);
  assert.deepEqual(Object.keys(row), expectedKeys);
  for (const key of expectedKeys) {
    assert.equal(typeof row[key], 'string', `${code}.${key}`);
    assert.ok(row[key].trim(), `${code}.${key} must not be blank`);
    assert.ok(!/[<>]/.test(row[key]), `${code}.${key} is plain text`);
    assert.ok(!/TODO|TBD|undefined/.test(row[key]), `${code}.${key} has no placeholders`);
    assert.equal(uiText(code, key), row[key]);
  }
  if (code !== 'en') {
    const different = expectedKeys.filter(key => row[key] !== UI_LANGUAGES_V22.en[key]);
    assert.ok(different.length > 40, `${code} must contain actual translated labels`);
  }
  assert.ok(Object.isFrozen(row));
}

// Language preference negotiation must work on first visit and saved preference.
for (const [input, output] of [
  ['zh-Hant', 'zh-TW'], ['zh-Hant-CN', 'zh-TW'], ['zh-HK', 'zh-TW'],
  ['zh-MO', 'zh-TW'], ['zh', 'zh-TW'], ['zh-Hans-TW', 'zh-CN'],
  ['zh-SG', 'zh-CN'], ['zh_CN', 'zh-CN'], ['en-US', 'en'],
  ['es-MX', 'es'], ['pt-BR', 'pt'], ['ja-JP', 'ja'], ['ar-EG', 'ar'],
  ['iw-IL', 'he'], ['in-ID', 'id'], ['tl-PH', 'fil'], ['nb-NO', 'no'],
]) assert.equal(resolveLanguage(input, ['de']), output, input);
assert.equal(resolveLanguage('auto', ['xx', 'ko-KR', 'en']), 'ko');
assert.equal(resolveLanguage('unknown', { languages: ['fr-CA'], language: 'en-US' }), 'fr');
assert.equal(resolveLanguage('de', ['ja-JP']), 'de');
assert.equal(resolveLanguage('auto', []), 'en');
assert.equal(resolveLanguage('auto', null), 'en');
for (const code of SUPPORTED_LANGUAGES_V22) assert.equal(resolveLanguage(code, []), code);

// Supported language does not falsely imply a bundled translation.
assert.equal(resolveLanguage('sw-KE', []), 'sw');
assert.equal(uiText('sw', 'help'), UI_LANGUAGES_V22.en.help);
assert.equal(uiText('xx', 'help'), UI_LANGUAGES_V22.en.help);
assert.equal(uiText('en', 'unknown-key'), 'unknown-key');
assert.equal(uiText('zh-HK', 'enter'), UI_LANGUAGES_V22['zh-TW'].enter);
const choices = languageChoices('en');
assert.equal(choices.length, 79);
assert.equal(choices.filter(x => x.bundled).length, 20);
assert.equal(choices.find(x => x.code === 'sw').bundled, false);
assert.ok(choices.every(x => x.value === x.code && typeof x.label === 'string' && x.label.trim()));
assert.equal(languageChoices('invalid_language').length, 79); // safe fallback on old/limited Intl
console.log('V22 HUD i18n: 900 translated labels, 79-code negotiation, fallback and selector checks passed.');
