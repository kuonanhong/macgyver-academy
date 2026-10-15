/* V12 regional pricing. Plans are defined in TWD (data/pricing.json); other
 * currencies are TWD × the weekly FX snapshot (data/fx.json), rounded UP to
 * the currency's minor unit. The server recomputes every charge, so these
 * figures are display estimates until the checkout quote is returned.
 * Location is inferred only from the browser time zone and language region —
 * no GPS or IP lookup. The learner can override the currency.
 */
const CURRENCY_KEY = 'mg-currency-v12';
const DEFAULT_PRICING = {
  version: 12, baseCurrency: 'TWD',
  plans: [
    {id: 'all-30', title: '30 天學習通行證', titleEn: '30-day learning pass', amountTwd: 299, durationDays: 30},
    {id: 'all-365', title: '365 天學習通行證', titleEn: '365-day learning pass', amountTwd: 2490, durationDays: 365}
  ],
  freePolicy: {freeStagesPerCourse: 1},
  chargeCurrencies: {paypal: ['AUD','CAD','CHF','CZK','DKK','EUR','GBP','HKD','HUF','ILS','JPY','MXN','NOK','NZD','PHP','PLN','SEK','SGD','THB','TWD','USD'], ecpay: ['TWD']},
  fallbackChargeCurrency: 'USD',
  zeroDecimal: ['BIF','CLP','DJF','GNF','HUF','IDR','ISK','JPY','KMF','KRW','MGA','PYG','RWF','TWD','UGX','VND','VUV','XAF','XOF','XPF'],
  fxMaxAgeDays: 10
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
const LANGUAGE_COUNTRY = {ja:'JP', ko:'KR', de:'DE', fr:'FR', it:'IT', es:'ES', pt:'BR', nl:'NL', sv:'SE', da:'DK', no:'NO', nb:'NO', fi:'FI', pl:'PL', cs:'CZ', sk:'SK', hu:'HU', ro:'RO', bg:'BG', el:'GR', tr:'TR', ru:'RU', uk:'UA', he:'IL', ar:'SA', fa:'IR', hi:'IN', bn:'BD', th:'TH', vi:'VN', id:'ID', ms:'MY', fil:'PH', tl:'PH', km:'KH', lo:'LA', my:'MM', mn:'MN', kk:'KZ', uz:'UZ', az:'AZ', ka:'GE', hy:'AM', sw:'KE', am:'ET', zu:'ZA', af:'ZA', is:'IS', et:'EE', lv:'LV', lt:'LT', sl:'SI', hr:'HR', sr:'RS', mk:'MK', sq:'AL', en:'US'};

let pricing = DEFAULT_PRICING, fx = {base: 'TWD', rates: {TWD: 1}, updatedAt: null, status: 'missing'}, loaded = null;

function storage() { try { return globalThis.localStorage; } catch { return null; } }
function country(tag) { const m = String(tag || '').replaceAll('_', '-').match(/-([A-Za-z]{2})(?:-|$)/); return m ? m[1].toUpperCase() : ''; }

/** Best-effort viewer country from time zone, then language region. */
export function detectCountry(env = globalThis) {
  let zone = '';
  try { zone = Intl.DateTimeFormat().resolvedOptions().timeZone || ''; } catch {}
  if (ZONE_COUNTRY[zone]) return {country: ZONE_COUNTRY[zone], basis: 'timezone', zone};
  const langs = [...(env.navigator?.languages || []), env.navigator?.language].filter(Boolean);
  for (const tag of langs) { const c = country(tag); if (c) return {country: c, basis: 'language', zone}; }
  const base = String(langs[0] || 'en').toLowerCase().split('-')[0];
  return {country: LANGUAGE_COUNTRY[base] || 'US', basis: 'language-default', zone};
}
export function currencyForCountry(code) { return COUNTRY_CURRENCY[String(code || '').toUpperCase()] || 'USD'; }

export async function loadPricing({fetchImpl = globalThis.fetch} = {}) {
  if (loaded) return loaded;
  loaded = (async () => {
    const data = globalThis.MG_DATA || {};
    try { pricing = data.pricing || await fetchImpl('data/pricing.json', {cache: 'no-cache'}).then(r => { if (!r.ok) throw Error(); return r.json(); }); } catch { pricing = DEFAULT_PRICING; }
    try { fx = data.fx || await fetchImpl('data/fx.json', {cache: 'no-cache'}).then(r => { if (!r.ok) throw Error(); return r.json(); }); } catch { fx = {base: 'TWD', rates: {TWD: 1}, updatedAt: null, status: 'missing'}; }
    if (!fx?.rates || typeof fx.rates !== 'object') fx = {base: 'TWD', rates: {TWD: 1}, updatedAt: null, status: 'missing'};
    fx.rates.TWD = 1;
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
/** TWD × rate rounded up to the minor unit; null when no rate is known. */
export function convertTwd(amountTwd, currency, rates = fx.rates) {
  if (currency === 'TWD') return amountTwd;
  const rate = Number(rates?.[currency]);
  if (!Number.isFinite(rate) || rate <= 0) return null;
  const scale = 10 ** minorDigits(currency);
  return Math.ceil(amountTwd * rate * scale - 1e-9) / scale;
}
export function formatMoney(amount, currency, locale) {
  if (amount === null || amount === undefined || !Number.isFinite(Number(amount))) return '—';
  const digits = minorDigits(currency);
  if (currency === 'TWD') { try { return 'NT$' + new Intl.NumberFormat(locale || undefined, {minimumFractionDigits: 0, maximumFractionDigits: 0}).format(amount); } catch { return 'NT$' + Math.round(amount); } }
  try { return new Intl.NumberFormat(locale || undefined, {style: 'currency', currency, currencyDisplay: 'symbol', minimumFractionDigits: digits, maximumFractionDigits: digits}).format(amount); }
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
