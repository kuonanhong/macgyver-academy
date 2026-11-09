// Browser-side Cloudflare adapter. Configuration contains an HTTPS origin only.
const CONSENT_KEY = 'mg-cloud-public-translation-v23';

export function mentorWorkerOrigin(value = globalThis.MG_CONFIG?.mentorWorkerUrl) {
  try {
    const url = new URL(value);
    return url.protocol === 'https:' && url.pathname === '/' && !url.username && !url.password &&
      !url.search && !url.hash ? url.origin : '';
  } catch {
    return '';
  }
}

export function mentorLineLink(value = globalThis.MG_CONFIG?.mentorLineUrl) {
  try {
    const url = new URL(value);
    if (url.protocol !== 'https:' || url.username || url.password || url.port || url.search || url.hash) return '';
    const valid = url.hostname === 'lin.ee' && /^\/[A-Za-z0-9_-]+$/.test(url.pathname)
      || url.hostname === 'line.me' && /^\/R\/ti\/p\/[@%A-Za-z0-9_-]+$/.test(url.pathname);
    return valid ? url.href : '';
  } catch {
    return '';
  }
}

export function cloudMentorRoute(language) {
  const destination = mentorWorkerOrigin();
  if (!destination) return null;
  return {
    id: 'cloudflare-mentor',
    label: String(language).startsWith('zh') ? 'Cloudflare 工程師傅' : 'Cloudflare engineering mentor',
    model: String(language).startsWith('zh') ? '站方配置的生成模型' : 'Operator-configured model',
    cloud: true,
    supportsImages: false,
    destination,
  };
}

const validId = value => typeof value === 'string' && /^[a-z0-9][a-z0-9_-]{0,99}$/i.test(value);
const httpUrl = value => {
  try {
    const url = new URL(value);
    return url.protocol === 'https:' && !url.username && !url.password ? url.href : '';
  } catch {
    return '';
  }
};

async function post(path, body, {signal, fetchImpl = globalThis.fetch} = {}) {
  const origin = mentorWorkerOrigin();
  if (!origin) throw Error('Cloudflare mentor is not configured.');
  const response = await fetchImpl(origin + path, {
    method: 'POST', headers: {'Content-Type': 'application/json', Accept: 'application/json'},
    body: JSON.stringify(body), credentials: 'omit', referrerPolicy: 'no-referrer',
    redirect: 'error', signal,
  });
  if (!response.ok) {
    const error = Error('Cloudflare HTTP ' + response.status);
    error.status = response.status;
    throw error;
  }
  return response.json();
}

export async function askCloudMentor({question, locale, context = {}, signal, fetchImpl} = {}) {
  const body = {question: String(question || '').slice(0, 1200), locale: String(locale || 'en').slice(0, 24)};
  // Never forward lesson text, personal notes, attachments, or chat history.
  const metadata = {
    domain: context.domain, courseId: context.courseId || context.projectId,
    sceneId: context.sceneId, station: context.station, stepId: context.stepId,
  };
  for (const [key, value] of Object.entries(metadata)) {
    if (validId(value)) body[key] = value;
    else if (key === 'station' && Number.isInteger(value) && value >= 0 && value <= 99) body[key] = value;
  }
  const result = await post('/api/mentor', body, {signal, fetchImpl});
  if (typeof result?.answer !== 'string' || !result.answer.trim()) throw Error('Cloudflare mentor returned an empty response.');
  const sources = Array.isArray(result.sources) ? result.sources.slice(0, 8).map(source => ({
    id: String(source?.id || '').slice(0, 160),
    title: [source?.reference, source?.title || source?.id].filter(value => typeof value === 'string' && value).join(' · ').slice(0, 300),
    url: httpUrl(source?.url),
  })).filter(source => source.id && source.title) : [];
  return {
    answer: result.answer.slice(0, 24000), sources, grounded: result.grounded === true,
    kind: result.mode === 'extract' ? 'extract' : 'generated',
    model: [result.provider, result.model].filter(value => typeof value === 'string').join(' · ').slice(0, 200),
  };
}

// Restrict DOM translation to the reviewed, first-stage-only static build.
export function cloudTranslationConfigured() {
  return globalThis.MG_PUBLIC_PREVIEW_ONLY === true &&
    globalThis.MG_CONFIG?.mentorCloudTranslation === true && Boolean(mentorWorkerOrigin());
}

let consentOrigin = '';
export function cloudTranslationAllowed() {
  if (!cloudTranslationConfigured()) return false;
  const origin = mentorWorkerOrigin();
  try { return consentOrigin === origin || sessionStorage.getItem(CONSENT_KEY) === origin; }
  catch { return consentOrigin === origin; }
}

export function allowCloudTranslation() {
  if (!cloudTranslationConfigured()) return false;
  consentOrigin = mentorWorkerOrigin();
  try { sessionStorage.setItem(CONSENT_KEY, consentOrigin); } catch { /* Session memory remains available. */ }
  return true;
}

export async function translatePublicText({language, texts, signal, fetchImpl}) {
  if (!cloudTranslationAllowed()) return null;
  const items = texts.map((text, i) => ({id: String(i), text}));
  const result = await post('/api/translate', {locale: language, items}, {signal, fetchImpl});
  if (!Array.isArray(result?.items) || result.items.length !== items.length) throw Error('Cloudflare translation was incomplete.');
  const translated = new Map(result.items.map(item => [String(item?.id), item?.text]));
  if (translated.size !== items.length) throw Error('Cloudflare translation returned duplicate IDs.');
  return {translations: items.map(item => translated.get(item.id))};
}
