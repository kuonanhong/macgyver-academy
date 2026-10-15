/* V13 regional pricing (HuaTuo-style exchange). Plans are defined in TWD
 * (data/pricing.json: NT$299 / 30 days, NT$2,490 / 365 days). Other currencies
 * are TWD × the most recent exchange rate, rounded UP to a tidy price with the
 * same rule as the server (supabase/functions/_shared/pricing.ts):
 *   zero-decimal currencies → whole units, then 10 / 100 / 1,000 steps for
 *   amounts ≥ 1,000 / 10,000 / 100,000;  two-decimal currencies ≥ 100 → whole
 *   units, below 100 → the next .49 or .99.
 * Rate sources, newest first: the site's Supabase fx_rates table (the rates the
 * server charges with), then the open ExchangeRate-API feed fetched in the
 * browser and cached for 12 hours, then the bundled weekly data/fx.json.
 * The region follows the viewer's language (語系): a language tied to one
 * country decides the currency; otherwise the time zone and the language region
 * decide. No GPS or IP lookup. The learner can override the currency, and the
 * server recomputes every charge.
 */
const CURRENCY_KEY = 'mg-currency-v12';
const LIVE_KEY = 'mg-fx-live-v13';
const LIVE_MAX_AGE_MS = 12 * 3600 * 1000;
const LIVE_SOURCES = [
  {url: 'https://open.er-api.com/v6/latest/TWD', name: 'ExchangeRate-API open access (open.er-api.com) — Rates By Exchange Rate API', attribution: 'https://www.exchangerate-api.com'},
  {url: 'https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/twd.json', name: 'fawazahmed0/exchange-api (jsDelivr)', attribution: 'https://github.com/fawazahmed0/exchange-api'}
];
const DEFAULT_PRICING = {
  version: 13, baseCurrency: 'TWD',
  plans: [
    {id: 'all-30', title: '30 天學習通行證', titleEn: '30-day learning pass', amountTwd: 299, durationDays: 30},
    {id: 'all-365', title: '365 天學習通行證', titleEn: '365-day learning pass', amountTwd: 2490, durationDays: 365}
  ],
  freePolicy: {freeStagesPerCourse: 1},
  chargeCurrencies: {paypal: ['AUD','CAD','CHF','CZK','DKK','EUR','GBP','HKD','HUF','ILS','JPY','MXN','NOK','NZD','PHP','PLN','SEK','SGD','THB','TWD','USD'], ecpay: ['TWD']},
  fallbackChargeCurrency: 'USD',
  zeroDecimal: ['BIF','CLP','DJF','GNF','HUF','IDR','ISK','JPY','KMF','KRW','MGA','PYG','RWF','TWD','UGX','VND','VUV','XAF','XOF','XPF'],
  fxMaxAgeDays: 3
};
/* Time zone → ISO country (major zones; others fall back to language region). */
const ZONE_COUNTRY = {
  'Asia/Taipei':'TW','Asia/Tokyo':'JP','Asia/Seoul':'KR','Asia/Shanghai':'CN','Asia/Chongqing':'CN','Asia/Urumqi':'CN','Asia/Hong_Kong':'HK','Asia/Macau':'MO','Asia/Singapore':'SG','Asia/Kuala_Lumpur':'MY','Asia/Kuching':'MY','Asia/Bangkok':'TH','Asia/Ho_Chi_Minh':'VN','Asia/Saigon':'VN','Asia/Jakarta':'ID','Asia/Makassar':'ID','Asia/Jayapura':'ID','Asia/Manila':'PH','Asia/Kolkata':'IN','Asia/Calcutta':'IN','Asia/Karachi':'PK','Asia/Dhaka':'BD','Asia/Colombo':'LK','Asia/Kathmandu':'NP','Asia/Yangon':'MM','Asia/Phnom_Penh':'KH','Asia/Vientiane':'LA','Asia/Ulaanbaatar':'MN','Asia/Almaty':'KZ','Asia/Tashkent':'UZ','Asia/Baku':'AZ','Asia/Tbilisi':'GE','Asia/Yerevan':'AM','Asia/Dubai':'AE','Asia/Riyadh':'SA','Asia/Qatar':'QA','Asia/Kuwait':'KW','Asia/Bahrain':'BH','Asia/Muscat':'OM','Asia/Amman':'JO','Asia/Jerusalem':'IL','Asia/Tel_Aviv':'IL','Asia/Tehran':'IR','Asia/Baghdad':'IQ','Asia/Beirut':'LB',
  'Europe/London':'GB','Europe/Dublin':'IE','Europe/Lisbon':'PT','Europe/Madrid':'ES','Europe/Paris':'FR','Europe/Brussels':'BE','Europe/Amsterdam':'NL','Europe/Luxembourg':'LU','Europe/Berlin':'DE','Europe/Zurich':'CH','Europe/Vienna':'AT','Europe/Rome':'IT','Europe/Malta':'MT','Europe/Copenhagen':'DK','Europe/Oslo':'NO','Europe/Stockholm':'SE','Europe/Helsinki':'FI','Europe/Tallinn':'EE','Europe/Riga':'LV','Europe/Vilnius':'LT','Europe/Warsaw':'PL','Europe/Prague':'CZ','Europe/Bratislava':'SK','Europe/Budapest':'HU','Europe/Ljubljana':'SI','Europe/Zagreb':'HR','Europe/Belgrade':'RS','Europe/Sarajevo':'BA','Europe/Skopje':'MK','Europe/Tirane':'AL','Europe/Athens':'GR','Europe/Sofia':'BG','Europe/Bucharest':'RO','Europe/Chisinau':'MD','Europe/Kiev':'UA','Europe/Kyiv':'UA','Europe/Minsk':'BY','Europe/Moscow':'RU','Europe/Istanbul':'TR','Atlantic/Reykjavik':'IS',
  'America/New_York':'US','America/Detroit':'US','America/Chicago':'US','America/Denver':'US','America/Phoenix':'US','America/Los_Angeles':'US','America/Anchorage':'US','Pacific/Honolulu':'US','America/Toronto':'CA','America/Vancouver':'CA','America/Edmonton':'CA','America/Winnipeg':'CA','America/Halifax':'CA','America/Mexico_City':'MX','America/Monterrey':'MX','America/Tijuana':'MX','America/Bogota':'CO','America/Lima':'PE','America/Santiago':'CL','America/Argentina/Buenos_Aires':'AR','America/Buenos_Aires':'AR','America/Sao_Paulo':'BR','America/Manaus':'BR','America/Caracas':'VE','America/Montevideo':'UY','America/Asuncion':'PY','America/La_Paz':'BO','America/Guayaquil':'EC','America/Panama':'PA','America/Costa_Rica':'CR','America/Guatemala':'GT','America/Santo_Domingo':'DO',
  'Australia/Sydney':'AU','Australia/Melbourne':'AU','Australia/Brisbane':'AU','Australia/Perth':'AU','Australia/Adelaide':'AU','Australia/Hobart':'AU','Australia/Darwin':'AU','Pacific/Auckland':'NZ','Pacific/Fiji':'FJ',
  'Africa/Johannesburg':'ZA','Africa/Lagos':'NG','Africa/Nairobi':'KE','Africa/Cairo':'EG','Africa/Casablanca':'MA','Africa/Algiers':'DZ','Africa/Tunis':'TN','Africa/Accra':'GH','Africa/Addis_Ababa':'ET','Africa/Dar_es_Salaam':'TZ','Africa/Kampala':'UG','Africa/Kigali':'RW','Africa/Dakar':'SN','Africa/Abidjan':'CI'
};
const EURO = 'AT BE CY DE EE ES FI FR GR HR IE IT LT LU LV MT NL PT SI SK'.split(' ');
const COUNTRY_CURRENCY = Object.assign(Object.fromEntries(EURO.map(c => [c, 'EUR'])), {
  TW:'TWD', JP:'JPY', KR:'KRW', CN:'CNY', HK:'HKD', MO:'MOP', SG:'SGD', MY:'MYR', TH:'THB', VN:'VND', ID:'IDR', PH:'PHP', IN:'INR', PK:'PKR', BD:'BDT', LK:'LKR', NP:'NPR', MM:'MMK', KH:'KHR', LA:'LAK', MN:'MNT', KZ:'KZT', UZ:'UZS', AZ:'AZN', GE:'GEL', AM:'AMD', AE:'AED', SA:'SAR', QA:'QAR', KW:'KWD', BH:'BHD', OM:'OMR', JO:'JOD', IL:'ILS', IR:'IRR', IQ:'IQD', LB:'LBP',
  GB:'GBP', CH:'CHF', LI:'CHF', DK:'DKK', NO:'NOK', SE:'SEK', IS:'ISK', PL:'PLN', CZ:'CZK', HU:'HUF', RS:'RSD', BA:'BAM', MK:'MKD', AL:'ALL', BG:'BGN', RO:'RON', MD:'MDL', UA:'UAH', BY:'BYN', RU:'RUB', TR:'TRY',
  US:'USD', CA:'CAD', MX:'MXN', CO:'COP', PE:'PEN', CL:'CLP', AR:'ARS', BR:'BRL', VE:'VES', UY:'UYU', PY:'PYG', BO:'BOB', EC:'USD', PA:'USD', CR:'CRC', GT:'GTQ', DO:'DOP', SV:'USD', PR:'USD',
  AU:'AUD', NZ:'NZD', FJ:'FJD', ZA:'ZAR', NG:'NGN', KE:'KES', EG:'EGP', MA:'MAD', DZ:'DZD', TN:'TND', GH:'GHS', ET:'ETB', TZ:'TZS', UG:'UGX', RW:'RWF', SN:'XOF', CI:'XOF'
});
/* Language without a region → most common country for currency purposes. */
/* Languages spoken mainly in one country: the language alone decides the region. */
const SINGLE_COUNTRY_LANGUAGES = new Set(['ja','ko','th','vi','id','he','el','tr','pl','cs','sk','hu','ro','bg','uk','ka','hy','az','kk','uz','mn','km','lo','my','ne','si','is','et','lv','lt','sl','hr','sr','mk','sq','bs','da','sv','no','nb','fi','fil','tl','am','hi','mr','gu','kn','ml','te','fa','af','zu','ha','yo','ig','so','mt','ga','cy','eu','gl','ca']);
const LANGUAGE_COUNTRY = {ja:'JP', ko:'KR', de:'DE', fr:'FR', it:'IT', es:'ES', pt:'BR', nl:'NL', sv:'SE', da:'DK', no:'NO', nb:'NO', fi:'FI', pl:'PL', cs:'CZ', sk:'SK', hu:'HU', ro:'RO', bg:'BG', el:'GR', tr:'TR', ru:'RU', uk:'UA', he:'IL', ar:'SA', fa:'IR', hi:'IN', bn:'BD', th:'TH', vi:'VN', id:'ID', ms:'MY', fil:'PH', tl:'PH', km:'KH', lo:'LA', my:'MM', mn:'MN', kk:'KZ', uz:'UZ', az:'AZ', ka:'GE', hy:'AM', sw:'KE', am:'ET', zu:'ZA', af:'ZA', is:'IS', et:'EE', lv:'LV', lt:'LT', sl:'SI', hr:'HR', sr:'RS', mk:'MK', sq:'AL', bs:'BA', ne:'NP', si:'LK', mr:'IN', gu:'IN', kn:'IN', ml:'IN', te:'IN', ta:'IN', pa:'IN', ur:'PK', ha:'NG', yo:'NG', ig:'NG', so:'SO', mt:'MT', ga:'IE', cy:'GB', eu:'ES', gl:'ES', ca:'ES', zh:'TW', en:'US'};

let pricing = DEFAULT_PRICING, fx = {base: 'TWD', rates: {TWD: 1}, updatedAt: null, status: 'missing'}, loaded = null;

function storage() { try { return globalThis.localStorage; } catch { return null; } }
function country(tag) { const m = String(tag || '').replaceAll('_', '-').match(/-([A-Za-z]{2})(?:-|$)/); return m ? m[1].toUpperCase() : ''; }

let languageProvider = () => '';
/** The app tells pricing which interface language the viewer chose (語系). */
export function setLanguageProvider(fn) { languageProvider = typeof fn === 'function' ? fn : () => ''; }

/** Best-effort viewer country: interface language first (like HuaTuo), then time zone, then browser language region. */
export function detectCountry(env = globalThis, uiLanguage = languageProvider()) {
  let zone = '';
  try { zone = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch {}
  const ui = String(uiLanguage || '').replaceAll('_', '-');
  const uiRegion = country(ui), uiBase = ui.toLowerCase().split('-')[0];
  if (uiRegion && uiRegion !== 'HANT' && uiRegion !== 'HANS') return {country: uiRegion, basis: 'language', zone};
  if (uiBase && SINGLE_COUNTRY_LANGUAGES.has(uiBase) && LANGUAGE_COUNTRY[uiBase]) return {country: LANGUAGE_COUNTRY[uiBase], basis: 'language', zone};
  if (ZONE_COUNTRY[zone]) return {country: ZONE_COUNTRY[zone], basis: 'timezone', zone};
  const langs = [...(env.navigator?.languages || []), env.navigator?.language].filter(Boolean);
  for (const tag of langs) { const c = country(tag); if (c) return {country: c, basis: 'language', zone}; }
  const base = uiBase || String(langs[0] || 'en').toLowerCase().split('-')[0];
  return {country: LANGUAGE_COUNTRY[base] || 'US', basis: 'language-default', zone};
}
export function currencyForCountry(code) { return COUNTRY_CURRENCY[String(code || '').toUpperCase()] || 'USD'; }

function cleanRates(raw) {
  const out = {};
  for (const [k, v] of Object.entries(raw || {})) { const c = String(k).toUpperCase(), n = Number(v); if (/^[A-Z]{3}$/.test(c) && Number.isFinite(n) && n > 0) out[c] = n; }
  out.TWD = 1;
  return out;
}
function saneRates(rates) { return Object.keys(rates).length >= 20 && rates.USD > 0.005 && rates.USD < 0.1; }
function newer(candidate) { return Date.parse(candidate.updatedAt || '') > Date.parse(fx.updatedAt || '') || !fx.updatedAt; }
function adopt(candidate) {
  if (!candidate || !saneRates(candidate.rates)) return false;
  if (!newer(candidate) && candidate.authoritative !== true) return false;
  fx = candidate;
  try { globalThis.dispatchEvent?.(new CustomEvent('mg:fx-updated', {detail: {source: fx.source, updatedAt: fx.updatedAt}})); } catch {}
  return true;
}
/** Rates the server charges with (Supabase fx_rates, readable with the public anon key). */
async function cloudRates(fetchImpl) {
  const cfg = globalThis.MG_CONFIG || globalThis.MACGYVER_CONFIG || {};
  const url = String(cfg.supabaseUrl || '').replace(/\/$/, ''), key = cfg.supabaseAnonKey || cfg.supabasePublishableKey || '';
  if (!/^https:\/\//.test(url) || !key) return null;
  const rows = await fetchImpl(`${url}/rest/v1/fx_rates?select=currency,per_twd,updated_at`, {headers: {apikey: key, authorization: `Bearer ${key}`}}).then(r => { if (!r.ok) throw Error(); return r.json(); });
  if (!Array.isArray(rows) || !rows.length) return null;
  const rates = cleanRates(Object.fromEntries(rows.map(r => [r.currency, r.per_twd])));
  const updatedAt = rows.filter(r => r.currency !== 'TWD').map(r => r.updated_at).sort().pop() || null;
  if (!updatedAt || (Date.now() - Date.parse(updatedAt)) > (pricing.fxMaxAgeDays || 3) * 86400000) return null;
  return {version: 13, base: 'TWD', status: 'server', authoritative: true, updatedAt, source: 'Site server rates (Supabase fx_rates, refreshed every 12 hours)', rates};
}
/** Browser-side live rates with a 12-hour cache, as in the HuaTuo academy. */
async function liveRates(fetchImpl) {
  try {
    const cached = JSON.parse(storage()?.getItem(LIVE_KEY) || 'null');
    if (cached?.rates && Date.now() - Number(cached.fetchedAt || 0) < LIVE_MAX_AGE_MS && saneRates(cleanRates(cached.rates))) return {...cached, rates: cleanRates(cached.rates)};
  } catch {}
  for (const src of LIVE_SOURCES) {
    try {
      const ctrl = typeof AbortController === 'function' ? new AbortController() : null;
      const timer = ctrl ? setTimeout(() => ctrl.abort(), 6000) : null;
      const doc = await fetchImpl(src.url, {cache: 'no-store', signal: ctrl?.signal}).then(r => { if (!r.ok) throw Error(); return r.json(); }).finally(() => timer && clearTimeout(timer));
      let rates, updatedAt;
      if (doc?.result === 'success' && doc.base_code === 'TWD') { rates = cleanRates(doc.rates); updatedAt = new Date(Number(doc.time_last_update_unix) * 1000).toISOString(); }
      else if (doc?.twd && doc.date) { rates = cleanRates(doc.twd); updatedAt = `${doc.date}T00:00:00Z`; }
      if (!rates || !saneRates(rates)) continue;
      const live = {version: 13, base: 'TWD', status: 'live', updatedAt, fetchedAt: Date.now(), source: src.name, attribution: src.attribution, rates};
      try { storage()?.setItem(LIVE_KEY, JSON.stringify(live)); } catch {}
      return live;
    } catch {}
  }
  return null;
}
let refreshing = null;
/** Look for newer rates without blocking the page for long. */
export function refreshRates({fetchImpl = globalThis.fetch, waitMs = 2500} = {}) {
  if (typeof fetchImpl !== 'function' || globalThis.location?.protocol === 'file:' && !globalThis.navigator?.onLine) return Promise.resolve(fx);
  if (!refreshing) refreshing = (async () => {
    try { if (adopt(await cloudRates(fetchImpl))) return fx; } catch {}
    try { adopt(await liveRates(fetchImpl)); } catch {}
    return fx;
  })();
  return Promise.race([refreshing, new Promise(resolve => setTimeout(() => resolve(fx), waitMs))]);
}

export async function loadPricing({fetchImpl = globalThis.fetch, live = true} = {}) {
  if (loaded) return loaded;
  loaded = (async () => {
    const data = globalThis.MG_DATA || {};
    try { pricing = data.pricing || await fetchImpl('data/pricing.json', {cache: 'no-cache'}).then(r => { if (!r.ok) throw Error(); return r.json(); }); } catch { pricing = DEFAULT_PRICING; }
    try { fx = data.fx || await fetchImpl('data/fx.json', {cache: 'no-cache'}).then(r => { if (!r.ok) throw Error(); return r.json(); }); } catch { fx = {base: 'TWD', rates: {TWD: 1}, updatedAt: null, status: 'missing'}; }
    if (!fx?.rates || typeof fx.rates !== 'object') fx = {base: 'TWD', rates: {TWD: 1}, updatedAt: null, status: 'missing'};
    fx = {...fx, rates: {...fx.rates, TWD: 1}};
    if (live) await refreshRates({fetchImpl});
    return {pricing, fx};
  })();
  return loaded;
}
export function pricingState() { return {pricing, fx}; }
export function plans() { return pricing.plans || DEFAULT_PRICING.plans; }
export function freeStages() { const n = Number(pricing.freePolicy?.freeStagesPerCourse); return Number.isInteger(n) && n >= 0 ? n : 1; }

export function minorDigits(currency) {
  if ((pricing.zeroDecimal || DEFAULT_PRICING.zeroDecimal).includes(currency)) return 0;
  if (['BHD', 'JOD', 'KWD', 'OMR', 'TND', 'IQD', 'LYD'].includes(currency)) return 3;
  return 2;
}
/** HuaTuo-style tidy price, never below TWD × rate (mirrors amountFor() on the server). */
export function tidyPrice(value, digits) {
  if (!Number.isFinite(value) || value <= 0) return null;
  const eps = 1e-9;
  if (digits === 0) {
    const mag = value >= 100000 ? 1000 : value >= 10000 ? 100 : value >= 1000 ? 10 : 1;
    return Math.ceil(value / mag - eps) * mag;
  }
  if (value >= 100) return Math.ceil(value - eps);
  const k = Math.ceil((value * 100 + 1) / 50 - eps);
  return Math.round(k * 50 - 1) / 100;
}
/** TWD × rate as a tidy local price; null when no rate is known. */
export function convertTwd(amountTwd, currency, rates = fx.rates) {
  if (currency === 'TWD') return amountTwd;
  const rate = Number(rates?.[currency]);
  if (!Number.isFinite(rate) || rate <= 0) return null;
  return tidyPrice(amountTwd * rate, minorDigits(currency) === 0 ? 0 : 2);
}
export function formatMoney(amount, currency, locale) {
  if (amount === null || amount === undefined || !Number.isFinite(Number(amount))) return '—';
  const digits = minorDigits(currency);
  if (currency === 'TWD') { try { return 'NT$' + new Intl.NumberFormat(locale || undefined, {minimumFractionDigits: 0, maximumFractionDigits: 0}).format(amount); } catch { return 'NT$' + Math.round(amount); } }
  const shown = Number.isInteger(Number(amount)) && Number(amount) >= 100 ? 0 : digits;
  try { return new Intl.NumberFormat(locale || undefined, {style: 'currency', currency, currencyDisplay: 'symbol', minimumFractionDigits: shown, maximumFractionDigits: shown}).format(amount); }
  catch { return `${currency} ${Number(amount).toFixed(minorDigits(currency))}`; }
}
export function availableCurrencies() {
  const known = new Set(Object.keys(fx.rates || {}).filter(c => /^[A-Z]{3}$/.test(c)));
  const preferred = ['TWD', 'USD', 'EUR', 'JPY', 'KRW', 'CNY', 'HKD', 'SGD', 'GBP', 'AUD', 'CAD'];
  return [...new Set([...preferred.filter(c => known.has(c)), ...[...known].sort()])];
}
export function selectedCurrency(env = globalThis) {
  let saved = '';
  try { saved = storage()?.getItem(CURRENCY_KEY) || ''; } catch {}
  if (/^[A-Z]{3}$/.test(saved) && (saved === 'TWD' || fx.rates?.[saved])) return {currency: saved, basis: 'manual'};
  const where = detectCountry(env), currency = currencyForCountry(where.country);
  return {currency: currency === 'TWD' || fx.rates?.[currency] ? currency : 'USD', basis: where.basis, country: where.country, zone: where.zone};
}
export function setCurrency(code) { try { if (/^[A-Z]{3}$/.test(code)) storage()?.setItem(CURRENCY_KEY, code); else storage()?.removeItem(CURRENCY_KEY); } catch {} }
/** Currency that will actually be charged for a provider. */
export function chargeCurrency(provider, wanted) {
  const list = pricing.chargeCurrencies?.[provider] || [];
  if (list.includes(wanted)) return wanted;
  return provider === 'ecpay' ? 'TWD' : (pricing.fallbackChargeCurrency || 'USD');
}
export function fxAgeDays(now = Date.now()) {
  const t = Date.parse(fx.updatedAt || '');
  return Number.isFinite(t) ? Math.max(0, (now - t) / 86400000) : Infinity;
}
export function priceTable(currency, locale) {
  return plans().map(plan => {
    const local = convertTwd(plan.amountTwd, currency);
    return {...plan, currency, amount: local, display: formatMoney(local, currency, locale), twdDisplay: formatMoney(plan.amountTwd, 'TWD', locale)};
  });
}
