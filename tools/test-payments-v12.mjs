#!/usr/bin/env node
// Payments V12 tests. Run from the project root:
//   node tools/test-payments-v12.mjs        (Node >= 22.18 strips TypeScript natively)
//   node --import tsx tools/test-payments-v12.mjs   (when tsx is installed in the project)
// Falls back to tsx from ./node_modules or /opt/npm-tools/node_modules automatically.
// No network: PayPal, ECPay, GoTrue and the FX source are fake `fetch` routes.
import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import { existsSync, readFileSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');
const FN = join(ROOT, 'supabase/functions/_shared');

async function enableTypeScript() {
  if (process.features?.typescript) return;
  for (const base of [join(ROOT, 'node_modules'), '/opt/npm-tools/node_modules']) {
    const api = join(base, 'tsx/dist/esm/api/index.mjs');
    if (existsSync(api)) {
      (await import(pathToFileURL(api).href)).register();
      return;
    }
  }
  throw new Error('Needs Node >= 22.18 (built-in type stripping) or tsx.');
}
await enableTypeScript();
const load = (rel) => import(pathToFileURL(join(FN, rel)).href);

const pricing = await load('pricing.ts');
const ecpay = await load('ecpay.ts');
const paypal = await load('paypal.ts');
const http = await load('http.ts');
const cors = await load('cors.ts');
const { loadConfig } = await load('config.ts');
const { makeCheckoutCreate, makeCheckoutCapture } = await load('handlers/checkout.ts');
const { makePayPalWebhook } = await load('handlers/paypal-webhook.ts');
const { makeEcpayNotify } = await load('handlers/ecpay-notify.ts');
const { makeUsernameLogin, makeAccess, makeFxRefresh, FX_SOURCE_URL } = await load('handlers/account.ts');
const sync = await import(pathToFileURL(join(ROOT, 'tools/payments-v12/sync-pricing.mjs')).href);

const tests = [];
const test = (name, fn) => tests.push([name, fn]);

// ---------------------------------------------------------------- fixtures
const NOW = new Date('2026-10-15T08:00:00.000Z');
const DAY = 86_400_000;
const KEY = 'pwFHCqoQZGmho4w6'; // ECPay public sandbox credentials (merchant 3002607)
const IV = 'EkRm7iFT261dpevs';
const ENV = {
  SUPABASE_URL: 'https://proj.supabase.co',
  SUPABASE_ANON_KEY: 'anon-key-for-tests',
  SUPABASE_SERVICE_ROLE_KEY: 'service-role-key-for-tests',
  ALLOWED_ORIGINS: 'https://kuonanhong.github.io, http://localhost:8080, javascript:alert(1)',
  SITE_URL: 'https://kuonanhong.github.io/macgyver-academy/',
  PAYPAL_ENV: 'sandbox',
  PAYPAL_CLIENT_ID: 'paypal-client-id',
  PAYPAL_CLIENT_SECRET: 'paypal-client-secret',
  PAYPAL_WEBHOOK_ID: '8PT597110X687430LKGECATA',
  ECPAY_ENV: 'sandbox',
  ECPAY_MERCHANT_ID: '3002607',
  ECPAY_HASH_KEY: KEY,
  ECPAY_HASH_IV: IV,
  CRON_SECRET: 'cron-secret-0123456789abcdef',
  TERMS_VERSION: 'v12-2026-10',
};
const ORIGIN = 'https://kuonanhong.github.io';
const USER_A = '00000000-0000-0000-0000-00000000000a';
const USER_B = '00000000-0000-0000-0000-00000000000b';
const TOKEN_A = 'eyJhbGciOiJIUzI1NiJ9.user-a.signature';
const TOKEN_B = 'eyJhbGciOiJIUzI1NiJ9.user-b.signature';
const TOKEN_UNCONFIRMED = 'eyJhbGciOiJIUzI1NiJ9.user-c.signature';
const PP_ORDER = '5O190127TN364715T';
const PP_CAPTURE = '3C679366HH908993F';

function fakeStore() {
  const s = {
    users: new Map([[TOKEN_A, { id: USER_A, emailConfirmed: true }], [TOKEN_B, { id: USER_B, emailConfirmed: true }], [TOKEN_UNCONFIRMED, { id: 'c', emailConfirmed: false }]]),
    plans: new Map(pricing.DEFAULT_RULES.plans.map((p) => [p.id, { id: p.id, amount_twd: p.amountTwd, duration_days: p.durationDays, active: true }])),
    fx: new Map([
      ['USD', { per_twd: 0.0312, updated_at: new Date(NOW - DAY).toISOString() }],
      ['JPY', { per_twd: 4.6512, updated_at: new Date(NOW - 2 * DAY).toISOString() }],
      ['EUR', { per_twd: 0.02857, updated_at: new Date(NOW - 11 * DAY).toISOString() }], // stale
    ]),
    orders: new Map(),
    ents: new Map(),
    events: new Map(),
    attempts: new Map(),
    usernames: new Map([['alice_01', 'alice@example.com'], ['bob', 'unconfirmed@example.com']]),
    fxRows: [],
    grants: 0,
    revokes: 0,
  };
  const accessFor = (uid) => {
    const mine = [...s.ents.values()].filter((e) => e.user_id === uid && !e.revoked_at);
    const current = mine.filter((e) => e.starts_at <= NOW && e.expires_at > NOW).sort((a, b) => b.expires_at - a.expires_at)[0];
    const last = mine.sort((a, b) => b.expires_at - a.expires_at)[0];
    return { active: !!current, expiresAt: last ? last.expires_at.toISOString() : null, planId: current?.plan_id ?? last?.plan_id ?? null };
  };
  const api = {
    async getUser(t) { return s.users.get(t) ?? null; },
    async myAccess(t) { return accessFor(s.users.get(t)?.id); },
    async getPlanRow(id) { return s.plans.get(id) ?? null; },
    async getFxRate(c) { return s.fx.get(c) ?? null; },
    async countRecentOrders(uid, since) { return [...s.orders.values()].filter((o) => o.user_id === uid && o.created_at >= since).length; },
    async insertOrder(row) {
      assert.ok(!s.orders.has(row.id));
      assert.match(row.id, /^MG[0-9A-F]{18}$/);
      s.orders.set(row.id, { ...row, provider_order_id: null, provider_capture_id: null, last_error: null, created_at: NOW, paid_at: null });
    },
    async getOrder(id) { const o = s.orders.get(id); return o ? { ...o } : null; },
    async findOrderBy(provider, field, value) { const o = [...s.orders.values()].find((x) => x.provider === provider && x[field] === value); return o ? { ...o } : null; },
    async updateOrder(id, patch, only) {
      const o = s.orders.get(id);
      if (!o || (only && !only.includes(o.status))) return false;
      if (patch.provider_capture_id && [...s.orders.values()].some((x) => x.id !== id && x.provider === o.provider && x.provider_capture_id === patch.provider_capture_id)) throw new Error('unique violation');
      Object.assign(o, patch);
      return true;
    },
    async grant(orderId) {
      const o = s.orders.get(orderId);
      if (['refunded', 'reversed', 'revoked'].includes(o.status)) return { granted: false, status: o.status, orderId };
      let e = s.ents.get(orderId);
      if (!e) {
        const mine = [...s.ents.values()].filter((x) => x.user_id === o.user_id && !x.revoked_at);
        const start = new Date(Math.max(NOW.getTime(), ...mine.map((x) => x.expires_at.getTime())));
        e = { order_id: orderId, user_id: o.user_id, plan_id: o.plan_id, starts_at: start, expires_at: new Date(start.getTime() + o.duration_days * DAY), revoked_at: null };
        s.ents.set(orderId, e);
        s.grants++;
      }
      o.status = 'paid';
      return { granted: true, status: 'paid', orderId, startsAt: e.starts_at.toISOString(), expiresAt: e.expires_at.toISOString(), accessExpiresAt: accessFor(o.user_id).expiresAt };
    },
    async revoke(orderId, reason) {
      const o = s.orders.get(orderId);
      if (!['refunded', 'reversed', 'revoked'].includes(o.status)) o.status = /^refund/i.test(reason) ? 'refunded' : /^(revers|chargeback)/i.test(reason) ? 'reversed' : 'revoked';
      const e = s.ents.get(orderId);
      if (e && !e.revoked_at) { e.revoked_at = NOW; s.revokes++; }
      return { revoked: true, status: o.status };
    },
    async hasEvent(p, k) { return s.events.has(`${p}:${k}`); },
    async recordEvent(e) { if (!s.events.has(`${e.provider}:${e.event_key}`)) s.events.set(`${e.provider}:${e.event_key}`, e); },
    async emailForUsername(u) { return s.usernames.get(u.toLowerCase()) ?? null; },
    async loginAttempt(key, limit) {
      const n = s.attempts.get(key) ?? 0;
      if (n >= limit) return { allowed: false, retryAfter: 600 };
      s.attempts.set(key, n + 1);
      return { allowed: true, retryAfter: 0 };
    },
    async clearLoginAttempts(key) { s.attempts.delete(key); },
    async upsertFxRates(rows) { s.fxRows.push(...rows); return rows.length; },
  };
  return { s, api };
}

/** Fake transport: routes by "METHOD url-prefix"; records every call. */
function fakeFetch(routes) {
  const calls = [];
  const fn = async (url, init = {}) => {
    const method = (init.method ?? 'GET').toUpperCase();
    const headers = new Headers(init.headers);
    const body = typeof init.body === 'string' ? init.body : init.body == null ? '' : String(init.body);
    calls.push({ method, url: String(url), headers, body });
    for (const [key, handler] of Object.entries(routes)) {
      const [m, prefix] = key.split(' ');
      if (m === method && String(url).startsWith(prefix)) {
        const out = await handler({ url: String(url), headers, body });
        if (out instanceof Response) return out;
        const status = out.status ?? 200;
        return typeof out.text === 'string'
          ? new Response(out.text, { status })
          : new Response(JSON.stringify(out.json), { status, headers: { 'Content-Type': 'application/json' } });
      }
    }
    throw new Error(`unexpected fetch ${method} ${url}`);
  };
  fn.calls = calls;
  return fn;
}

const PP = 'https://api-m.sandbox.paypal.com';
/** PayPal order id used in a /v2/checkout/orders/{id}/capture URL. */
const ppIdFrom = (url) => /orders\/([A-Z0-9]+)/.exec(url)?.[1];
const captureIdFor = (ppOrderId) => (ppOrderId === PP_ORDER ? PP_CAPTURE : `CAP${ppOrderId.slice(-12)}`);
function paypalRoutes(overrides = {}) {
  let created = 0;
  return {
    [`POST ${PP}/v1/oauth2/token`]: () => ({ json: { access_token: 'A21AAtesttoken', token_type: 'Bearer', expires_in: 32400 } }),
    [`POST ${PP}/v2/checkout/orders/`]: overrides.capture ?? (() => ({ status: 500, json: {} })),
    [`POST ${PP}/v2/checkout/orders`]: () => ({ status: 201, json: { id: ++created === 1 ? PP_ORDER : `PPORDER${String(created).padStart(10, '0')}`, status: 'CREATED' } }),
    [`GET ${PP}/v2/checkout/orders/`]: overrides.get ?? (() => ({ status: 404, json: {} })),
    [`POST ${PP}/v1/notifications/verify-webhook-signature`]: overrides.verify ?? (() => ({ json: { verification_status: 'SUCCESS' } })),
  };
}

function captureResponse(orderId, { value = '9.49', currency = 'USD', customId = orderId, status = 'COMPLETED', id = PP_ORDER, url } = {}) {
  if (url) id = ppIdFrom(url);
  return {
    id,
    status: status === 'COMPLETED' ? 'COMPLETED' : 'APPROVED',
    purchase_units: [{
      reference_id: orderId,
      payments: {
        captures: [{
          id: captureIdFor(id),
          status,
          amount: { currency_code: currency, value },
          final_capture: true,
          custom_id: customId,
          invoice_id: orderId,
          supplementary_data: { related_ids: { order_id: id } },
        }],
      },
    }],
  };
}

function request(method, url, { body, token, origin = ORIGIN, headers = {}, raw, contentType } = {}) {
  const h = new Headers(headers);
  if (origin) h.set('origin', origin);
  if (token) h.set('authorization', `Bearer ${token}`);
  let payload;
  if (raw !== undefined) {
    payload = raw;
    h.set('content-type', contentType ?? 'application/x-www-form-urlencoded');
  } else if (body !== undefined) {
    payload = JSON.stringify(body);
    h.set('content-type', 'application/json');
  }
  return new Request(url, { method, headers: h, body: payload });
}

function harness(routes = paypalRoutes(), env = ENV) {
  paypal.clearTokenCache();
  const { s, api } = fakeStore();
  const logs = [];
  const fetch = fakeFetch(routes);
  const deps = { config: loadConfig((k) => env[k]), store: api, fetch, now: () => NOW, log: (event, fields) => logs.push({ event, ...fields }) };
  return { s, deps, fetch, logs };
}

const F = 'https://proj.supabase.co/functions/v1';
const read = async (res) => ({ status: res.status, body: res.headers.get('content-type')?.includes('json') ? await res.json() : await res.text(), headers: res.headers });

// ------------------------------------------------------------------ pricing
test('generated pricing rules match public/academy/data/pricing.json', () => {
  const source = JSON.parse(readFileSync(join(ROOT, 'public/academy/data/pricing.json'), 'utf8'));
  assert.deepEqual(pricing.DEFAULT_RULES, sync.pickRules(source));
  assert.equal(readFileSync(sync.TARGET, 'utf8'), sync.render(sync.pickRules(source)), 'run node tools/payments-v12/sync-pricing.mjs');
  const migration = readFileSync(join(ROOT, 'supabase/002_accounts_commerce.sql'), 'utf8');
  for (const line of sync.plansSql(sync.pickRules(source)).split('\n').filter((l) => l.startsWith('  ('))) {
    assert.ok(migration.includes(line.replace(/,$/, '')), `002 plans seed differs from pricing.json: ${line}`);
  }
});

test('amountFor: TWD base and V13 tidy rounding (HuaTuo rule), exact decimals', () => {
  const r = { USD: 0.0312, JPY: '4.6512', EUR: 0.02857, HUF: 11.2, KRW: 41.75, X1: 0.07, X2: '2.9e-2' };
  assert.equal(pricing.amountFor(299, 'TWD', {}), '299');
  assert.equal(pricing.amountFor(2490, 'TWD', { TWD: 99 }), '2490'); // base currency ignores rates
  assert.equal(pricing.amountFor(299, 'USD', r), '9.49'); // 9.3288 → next .49
  assert.equal(pricing.amountFor(2490, 'USD', r), '77.99'); // 77.688 → next .99
  assert.equal(pricing.amountFor(299, 'USD', { USD: '0.0312' }), '9.49');
  assert.equal(pricing.amountFor(299, 'JPY', r), '1400'); // 1390.7 ≥ 1,000 → step 10
  assert.equal(pricing.amountFor(2490, 'JPY', r), '11600'); // 11581.5 ≥ 10,000 → step 100
  assert.equal(pricing.amountFor(299, 'KRW', r), '12500'); // 12483.25 → step 100
  assert.equal(pricing.amountFor(2490, 'KRW', r), '104000'); // 103957.5 ≥ 100,000 → step 1,000
  assert.equal(pricing.amountFor(299, 'EUR', r), '8.99'); // 8.54243 → next .99
  assert.equal(pricing.amountFor(299, 'HUF', r), '3350'); // 3348.8 → step 10 (HUF zero-decimal)
  assert.equal(pricing.amountFor(299, 'USD', { USD: 0.07 }), '20.99'); // 20.93 → 20.99
  assert.equal(pricing.amountFor(2490, 'USD', { USD: 0.001 }), '2.49'); // exactly .49 stays
  assert.equal(pricing.amountFor(299, 'USD', { USD: 0.0301 }), '9.49'); // 8.9999 → 9.49 (never below)
  assert.equal(pricing.amountFor(2490, 'USD', { USD: 0.05 }), '125.00'); // 124.5 ≥ 100 → whole units
  assert.equal(pricing.amountFor(299, 'USD', { USD: '2.9e-2' }), '8.99'); // exponent form
  assert.throws(() => pricing.amountFor(299, 'USD', {}), /No exchange rate/);
  assert.throws(() => pricing.amountFor(299, 'USD', { USD: -1 }), /Invalid decimal/);
  assert.throws(() => pricing.amountFor(0, 'TWD', {}), /Invalid plan amount/);
});

test('client tidyPrice() mirrors server amountFor()', async () => {
  const client = await import(pathToFileURL(join(ROOT, 'public/academy/pricing.js')).href);
  const rates = { USD: 0.0312, EUR: 0.02857, JPY: 4.6512, KRW: 41.75, HUF: 11.2, GBP: 0.0237, HKD: 0.2457, CNY: 0.2098, SGD: 0.0401 };
  for (const [cur, rate] of Object.entries(rates)) for (const twd of [299, 2490]) {
    const server = pricing.amountFor(twd, cur, rates);
    const shown = client.convertTwd(twd, cur, rates);
    assert.ok(pricing.sameAmount(server, String(shown), cur), `${cur} ${twd}: server ${server} vs client ${shown}`);
  }
});

test('chargeCurrency: PayPal list + USD fallback; ECPay TWD only', () => {
  assert.equal(pricing.chargeCurrency('paypal', 'usd'), 'USD');
  assert.equal(pricing.chargeCurrency('paypal', 'TWD'), 'TWD');
  assert.equal(pricing.chargeCurrency('paypal', 'JPY'), 'JPY');
  assert.equal(pricing.chargeCurrency('paypal', 'KRW'), 'USD'); // not a PayPal charge currency
  assert.equal(pricing.chargeCurrency('paypal', 'CNY'), 'USD');
  assert.equal(pricing.chargeCurrency('paypal', undefined), 'USD');
  assert.equal(pricing.chargeCurrency('ecpay', 'USD'), 'TWD');
  assert.throws(() => pricing.chargeCurrency('stripe', 'USD'), /Unknown payment provider/);
});

test('fx freshness, amount equality and fx currency list', () => {
  assert.equal(pricing.isRateFresh(new Date(NOW - 2 * DAY), NOW), true);
  assert.equal(pricing.isRateFresh(new Date(NOW - 4 * DAY), NOW), false);
  assert.equal(pricing.isRateFresh(null, NOW), false);
  assert.equal(pricing.sameAmount('9.30', 9.3, 'USD'), true);
  assert.equal(pricing.sameAmount('9.49', '9.50', 'USD'), false);
  assert.equal(pricing.sameAmount('280', '280.00', 'JPY'), true);
  assert.equal(pricing.sameAmount('280.5', '280', 'JPY'), false);
  const list = pricing.fxCurrencies();
  for (const c of pricing.DEFAULT_RULES.chargeCurrencies.paypal.filter((x) => x !== 'TWD')) assert.ok(list.includes(c), c);
  assert.ok(!list.includes('TWD') && list.includes('KRW') && list.includes('CNY'));
});

// ------------------------------------------------------- ECPay CheckMacValue
const officialVector = {
  fields: { ChoosePayment: 'ALL', EncryptType: 1, ItemName: 'Apple iphone 15', MerchantID: '3002607', MerchantTradeDate: '2023/03/12 15:30:23', MerchantTradeNo: 'ecpay20230312153023', PaymentType: 'aio', ReturnURL: 'https://www.ecpay.com.tw/receive.php', TotalAmount: 30000, TradeDesc: '促銷方案' },
  key: KEY, iv: IV,
};
const macCases = [
  officialVector,
  { fields: { MerchantID: '3002607', MerchantTradeNo: 'MG0123456789ABCDEF01', ItemName: 'MacGyver 工程學院 30 天學習通行證', TradeDesc: "tilde~ space 'quote' (paren) *star* !bang -_. +plus &amp; 100% #hash", TotalAmount: '299', CheckMacValue: 'IGNORED' }, key: KEY, iv: IV },
  { fields: { aField: 'x', Bfield: 'y', CustomField1: '', customfield2: 'Z', RtnMsg: '交易成功 Succeeded', PaymentDate: '2026/10/15 16:01:02', Emoji: '🚀 ok' }, key: '5294y06JbISpM5x9', iv: 'v77hoKGq4kWxNNIS' },
  { fields: {}, key: KEY, iv: IV },
];

function pythonMacs(cases) {
  const code = [
    'import json, sys',
    'sys.path.insert(0, sys.argv[1])',
    'from portable.commerce import check_mac',
    'cases = json.load(sys.stdin)',
    "print(json.dumps([check_mac(c['fields'], c['key'], c['iv']) for c in cases]))",
  ].join('\n');
  const out = spawnSync('python3', ['-I', '-c', code, ROOT], { input: JSON.stringify(cases), encoding: 'utf8' });
  if (out.status !== 0) throw new Error('python3 check_mac failed: ' + out.stderr);
  return JSON.parse(out.stdout);
}

test('checkMacValue is identical to Python portable/commerce.py check_mac', async () => {
  const aio = await ecpay.buildAioFields({
    env: 'sandbox', merchantId: '3002607', orderId: 'MG0123456789ABCDEF01', tradeDate: NOW, amount: 299,
    itemName: 'MacGyver 工程學院 30 天學習通行證', tradeDesc: 'MacGyver Engineering Academy learning pass',
    returnUrl: `${F}/ecpay-notify`, clientBackUrl: 'https://kuonanhong.github.io/macgyver-academy/?payment=ecpay&order=MG0123456789ABCDEF01',
  }, KEY, IV);
  const cases = [...macCases, { fields: aio.fields, key: KEY, iv: IV }];
  const expected = pythonMacs(cases);
  assert.equal(expected[0], '6C51C9E6888DE861FD62FB1DD17029FC742634498FD813DC43D4243B5685B840'); // ECPay documentation example
  for (let i = 0; i < cases.length; i++) {
    assert.equal(await ecpay.checkMacValue(cases[i].fields, cases[i].key, cases[i].iv), expected[i], `case ${i}`);
  }
  assert.equal(aio.fields.CheckMacValue, expected.at(-1));
  assert.equal(aio.action, 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5');
  assert.equal(aio.fields.MerchantTradeDate, '2026/10/15 16:00:00'); // Asia/Taipei
  assert.equal(aio.fields.ChoosePayment, 'Credit');
  assert.equal(aio.fields.EncryptType, '1');
});

test('ECPay notification parser is strict', () => {
  assert.deepEqual(ecpay.parseNotification('A=1&B=%E4%BA%A4+x&C='), { A: '1', B: '交 x', C: '' });
  for (const bad of ['', 'A=1&A=2', 'A=1&&B=2', '=1', 'A=%E4%BA', '1A=2', 'A', `${'A=1&'.repeat(100)}B=1`]) {
    assert.throws(() => ecpay.parseNotification(bad), ecpay.EcpayError, JSON.stringify(bad));
  }
});

// --------------------------------------------------------------- PayPal pure
test('PayPal token fetch: Basic auth, client_credentials, cached', async () => {
  paypal.clearTokenCache();
  const fetch = fakeFetch(paypalRoutes());
  const t1 = await paypal.getAccessToken({ fetch, env: 'sandbox', clientId: 'id', clientSecret: 'secret', now: () => NOW.getTime() });
  const t2 = await paypal.getAccessToken({ fetch, env: 'sandbox', clientId: 'id', clientSecret: 'secret', now: () => NOW.getTime() });
  assert.equal(t1, 'A21AAtesttoken');
  assert.equal(t2, t1);
  assert.equal(fetch.calls.length, 1);
  const c = fetch.calls[0];
  assert.equal(c.url, `${PP}/v1/oauth2/token`);
  assert.equal(c.headers.get('authorization'), 'Basic ' + Buffer.from('id:secret').toString('base64'));
  assert.equal(c.headers.get('content-type'), 'application/x-www-form-urlencoded');
  assert.equal(c.body, 'grant_type=client_credentials');
});

test('verify-webhook-signature request shape (raw event embedded verbatim)', async () => {
  const fetch = fakeFetch(paypalRoutes());
  const raw = '{"id":"WH-1","event_type":"PAYMENT.CAPTURE.COMPLETED","resource":{"amount":{"value":"9.30"},"n":1.10,"t":"中文"}}';
  const headers = new Headers({
    'paypal-auth-algo': 'SHA256withRSA',
    'paypal-cert-url': 'https://api.sandbox.paypal.com/v1/notifications/certs/CERT-360caa42-fca2a594-a5cafa77',
    'paypal-transmission-id': '103e3700-8b82-11ea-9a1e-3f7b8e4d2c1a',
    'paypal-transmission-sig': 'c2lnbmF0dXJl',
    'paypal-transmission-time': '2026-10-15T08:00:00Z',
  });
  assert.equal(await paypal.verifyWebhookSignature({ fetch, env: 'sandbox', accessToken: 'tok', webhookId: 'WEBHOOK123', headers, rawBody: raw }), true);
  const c = fetch.calls[0];
  assert.equal(c.method, 'POST');
  assert.equal(c.url, `${PP}/v1/notifications/verify-webhook-signature`);
  assert.equal(c.headers.get('authorization'), 'Bearer tok');
  assert.equal(c.headers.get('content-type'), 'application/json');
  const sent = JSON.parse(c.body);
  assert.deepEqual(Object.keys(sent), ['auth_algo', 'cert_url', 'transmission_id', 'transmission_sig', 'transmission_time', 'webhook_id', 'webhook_event']);
  assert.equal(sent.auth_algo, 'SHA256withRSA');
  assert.equal(sent.transmission_id, '103e3700-8b82-11ea-9a1e-3f7b8e4d2c1a');
  assert.equal(sent.webhook_id, 'WEBHOOK123');
  assert.ok(c.body.endsWith(`"webhook_event":${raw}}`), 'raw body must be embedded byte-for-byte');
  const failing = fakeFetch(paypalRoutes({ verify: () => ({ json: { verification_status: 'FAILURE' } }) }));
  assert.equal(await paypal.verifyWebhookSignature({ fetch: failing, env: 'sandbox', accessToken: 'tok', webhookId: 'W', headers, rawBody: raw }), false);
  const partial = new Headers(headers);
  partial.delete('paypal-transmission-sig');
  await assert.rejects(paypal.verifyWebhookSignature({ fetch, env: 'sandbox', accessToken: 'tok', webhookId: 'W', headers: partial, rawBody: raw }), /Missing PayPal transmission headers/);
  await assert.rejects(paypal.verifyWebhookSignature({ fetch, env: 'sandbox', accessToken: 'tok', webhookId: 'W', headers, rawBody: '[1]' }), /JSON object/);
});

test('capture verification rejects mismatched amount / currency / custom_id', () => {
  const id = 'MG0123456789ABCDEF01';
  const exp = { orderId: id, amount: '9.49', currency: 'USD', paypalOrderId: PP_ORDER };
  assert.deepEqual(paypal.verifyCapture(captureResponse(id), exp), { kind: 'completed', captureId: PP_CAPTURE });
  assert.deepEqual(paypal.verifyCapture(captureResponse(id), { ...exp, amount: 9.49 + '' }), { kind: 'completed', captureId: PP_CAPTURE });
  assert.deepEqual(paypal.verifyCapture(captureResponse(id, { value: '9.32' }), exp), { kind: 'mismatch', reason: 'amount' });
  assert.deepEqual(paypal.verifyCapture(captureResponse(id, { value: '93.30' }), exp), { kind: 'mismatch', reason: 'amount' });
  assert.deepEqual(paypal.verifyCapture(captureResponse(id, { currency: 'EUR' }), exp), { kind: 'mismatch', reason: 'currency' });
  assert.deepEqual(paypal.verifyCapture(captureResponse(id, { customId: 'MGFFFFFFFFFFFFFFFFFF' }), exp), { kind: 'mismatch', reason: 'custom_id' });
  const noCustom = captureResponse(id);
  delete noCustom.purchase_units[0].payments.captures[0].custom_id;
  assert.deepEqual(paypal.verifyCapture(noCustom, exp), { kind: 'mismatch', reason: 'custom_id' });
  assert.deepEqual(paypal.verifyCapture(captureResponse(id, { id: 'OTHERORDER123' }), exp), { kind: 'mismatch', reason: 'paypal_order' });
  assert.deepEqual(paypal.verifyCapture(captureResponse(id, { status: 'PENDING' }), exp), { kind: 'pending', captureId: PP_CAPTURE });
  assert.deepEqual(paypal.verifyCapture(captureResponse(id, { status: 'DECLINED' }), exp), { kind: 'declined', reason: 'DECLINED' });
  const two = captureResponse(id);
  two.purchase_units[0].payments.captures.push({ ...two.purchase_units[0].payments.captures[0], id: 'SECONDCAPTURE1' });
  assert.equal(paypal.verifyCapture(two, exp).kind, 'mismatch');
  assert.equal(paypal.verifyCapture({ id: PP_ORDER, status: 'COMPLETED', purchase_units: [{}] }, exp).kind, 'incomplete');
  const body = paypal.buildCreateOrderBody({ orderId: id, amount: '9.49', currency: 'USD', description: 'd', brandName: 'b' });
  assert.equal(body.intent, 'CAPTURE');
  assert.deepEqual(body.purchase_units[0].amount, { currency_code: 'USD', value: '9.49' });
  assert.equal(body.purchase_units[0].custom_id, id);
  assert.equal(body.purchase_units[0].invoice_id, id);
  assert.equal(paypal.relatedCaptureId({ links: [{ rel: 'self', href: `${PP}/v2/payments/refunds/R1` }, { rel: 'up', href: `${PP}/v2/payments/captures/${PP_CAPTURE}` }] }), PP_CAPTURE);
});

// ------------------------------------------------------------- CORS/config
test('CORS allowlist and config parsing', async () => {
  assert.deepEqual(cors.parseAllowedOrigins(ENV.ALLOWED_ORIGINS), ['https://kuonanhong.github.io', 'http://localhost:8080']);
  assert.deepEqual(cors.parseAllowedOrigins('https://a.example/path/, http://evil.example'), ['https://a.example']);
  const { deps } = harness();
  const create = makeCheckoutCreate(deps);
  const pre = await create(request('OPTIONS', `${F}/checkout-create`));
  assert.equal(pre.status, 204);
  assert.equal(pre.headers.get('access-control-allow-origin'), ORIGIN);
  assert.match(pre.headers.get('access-control-allow-headers'), /authorization/);
  assert.equal((await create(request('OPTIONS', `${F}/checkout-create`, { origin: 'https://evil.example' }))).status, 403);
  const denied = await read(await create(request('POST', `${F}/checkout-create`, { origin: 'https://evil.example', token: TOKEN_A, body: {} })));
  assert.equal(denied.status, 403);
  assert.equal(denied.headers.get('access-control-allow-origin'), null);
  const live = loadConfig((k) => ({ ...ENV, ECPAY_ENV: 'live' })[k]);
  assert.equal(live.ecpay, null, 'public test merchant must never run live');
  assert.equal(loadConfig((k) => ({ ...ENV, CRON_SECRET: 'short' })[k]).cronSecret, '');
  assert.equal(loadConfig((k) => ENV[k]).siteUrl, 'https://kuonanhong.github.io/macgyver-academy/');
});

// ----------------------------------------------------------- checkout-create
test('checkout-create validates auth, terms, plan and computes the price server-side', async () => {
  const { s, deps, fetch } = harness();
  const create = makeCheckoutCreate(deps);
  const call = (body, token = TOKEN_A) => create(request('POST', `${F}/checkout-create`, { token, body })).then(read);
  assert.equal((await call({ planId: 'all-30', provider: 'paypal', termsAccepted: true, termsVersion: 'v12-2026-10' }, null)).status, 401);
  assert.equal((await call({ planId: 'all-30', provider: 'paypal', termsAccepted: true, termsVersion: 'v12-2026-10' }, TOKEN_UNCONFIRMED)).body.error, 'email_not_confirmed');
  assert.equal((await call({ planId: 'all-30', provider: 'paypal', termsVersion: 'v12-2026-10' })).body.error, 'terms_required');
  const outdated = await call({ planId: 'all-30', provider: 'paypal', termsAccepted: true, termsVersion: 'v10-2026-10' });
  assert.equal(outdated.status, 409);
  assert.equal(outdated.body.termsVersion, 'v12-2026-10');
  assert.equal((await call({ planId: 'gold', provider: 'paypal', termsAccepted: true, termsVersion: 'v12-2026-10' })).body.error, 'invalid_plan');
  assert.equal((await call({ planId: 'all-30', provider: 'stripe', termsAccepted: true, termsVersion: 'v12-2026-10' })).body.error, 'invalid_provider');

  const ok = await call({ planId: 'all-30', provider: 'paypal', currency: 'usd', amount: '0.01', termsAccepted: true, termsVersion: 'v12-2026-10' });
  assert.equal(ok.status, 200);
  assert.deepEqual(Object.keys(ok.body).sort(), ['amount', 'currency', 'durationDays', 'orderId', 'paypalOrderId', 'planId', 'provider']);
  assert.equal(ok.body.amount, '9.49'); // client "amount" ignored
  assert.equal(ok.body.currency, 'USD');
  assert.equal(ok.body.paypalOrderId, PP_ORDER);
  assert.equal(ok.headers.get('access-control-allow-origin'), ORIGIN);
  const created = fetch.calls.find((c) => c.url === `${PP}/v2/checkout/orders`);
  const sent = JSON.parse(created.body);
  assert.deepEqual(sent.purchase_units[0].amount, { currency_code: 'USD', value: '9.49' });
  assert.equal(sent.purchase_units[0].custom_id, ok.body.orderId);
  assert.equal(created.headers.get('paypal-request-id'), `create-${ok.body.orderId}`);
  const row = s.orders.get(ok.body.orderId);
  assert.equal(row.status, 'pending');
  assert.equal(row.provider_order_id, PP_ORDER);
  assert.equal(row.amount, '9.49');
  assert.equal(row.amount_twd, 299);
  assert.equal(row.terms_version, 'v12-2026-10');

  const krw = await call({ planId: 'all-365', provider: 'paypal', currency: 'KRW', termsAccepted: true, termsVersion: 'v12-2026-10' });
  assert.equal(krw.body.currency, 'USD'); // fallback charge currency
  assert.equal(krw.body.amount, '77.99');
  const jpy = await call({ planId: 'all-30', provider: 'paypal', currency: 'JPY', termsAccepted: true, termsVersion: 'v12-2026-10' });
  assert.equal(jpy.body.amount, '1400');
  const stale = await call({ planId: 'all-30', provider: 'paypal', currency: 'EUR', termsAccepted: true, termsVersion: 'v12-2026-10' });
  assert.equal(stale.status, 503);
  assert.equal(stale.body.error, 'fx_unavailable');
  const twd = await call({ planId: 'all-30', provider: 'paypal', termsAccepted: true, termsVersion: 'v12-2026-10' });
  assert.equal(twd.body.currency, 'TWD');
  assert.equal(twd.body.amount, '299');

  s.plans.get('all-30').amount_twd = 199; // database not synced with pricing.json → fail closed
  assert.equal((await call({ planId: 'all-30', provider: 'paypal', termsAccepted: true, termsVersion: 'v12-2026-10' })).body.error, 'pricing_mismatch');
});

test('checkout-create for ECPay returns a signed AIO form', async () => {
  const { s, deps } = harness();
  const create = makeCheckoutCreate(deps);
  const res = await read(await create(request('POST', `${F}/checkout-create`, { token: TOKEN_A, body: { planId: 'all-365', provider: 'ecpay', currency: 'USD', termsAccepted: true, termsVersion: 'v12-2026-10' } })));
  assert.equal(res.status, 200);
  assert.equal(res.body.provider, 'ecpay');
  assert.equal(res.body.currency, 'TWD');
  assert.equal(res.body.amount, '2490');
  assert.equal(res.body.action, 'https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5');
  const f = res.body.fields;
  assert.equal(f.TotalAmount, '2490');
  assert.equal(f.MerchantTradeNo, res.body.orderId);
  assert.equal(f.ReturnURL, `${F}/ecpay-notify`);
  assert.equal(f.ClientBackURL, `https://kuonanhong.github.io/macgyver-academy/?payment=ecpay&order=${res.body.orderId}`);
  assert.equal(f.CheckMacValue, await ecpay.checkMacValue(f, KEY, IV));
  assert.equal(s.orders.get(res.body.orderId).currency, 'TWD');
});

test('checkout-create rate-limits orders per user', async () => {
  const { deps } = harness();
  const create = makeCheckoutCreate(deps);
  const body = { planId: 'all-30', provider: 'ecpay', termsAccepted: true, termsVersion: 'v12-2026-10' };
  for (let i = 0; i < 10; i++) assert.equal((await create(request('POST', `${F}/checkout-create`, { token: TOKEN_A, body }))).status, 200);
  const limited = await create(request('POST', `${F}/checkout-create`, { token: TOKEN_A, body }));
  assert.equal(limited.status, 429);
  assert.equal(limited.headers.get('retry-after'), '900');
});

// ---------------------------------------------------------- checkout-capture
async function paypalOrder(h) {
  const res = await read(await makeCheckoutCreate(h.deps)(request('POST', `${F}/checkout-create`, { token: TOKEN_A, body: { planId: 'all-30', provider: 'paypal', currency: 'USD', termsAccepted: true, termsVersion: 'v12-2026-10' } })));
  assert.equal(res.status, 200);
  return res.body.orderId;
}

test('checkout-capture verifies, grants once and is idempotent', async () => {
  let orderId;
  const h = harness(paypalRoutes({ capture: ({ url }) => ({ status: 201, json: captureResponse(orderId, { url }) }) }));
  orderId = await paypalOrder(h);
  const capture = makeCheckoutCapture(h.deps);
  const res = await read(await capture(request('POST', `${F}/checkout-capture`, { token: TOKEN_A, body: { orderId } })));
  assert.equal(res.status, 200);
  assert.equal(res.body.status, 'paid');
  assert.equal(res.body.expiresAt, new Date(NOW.getTime() + 30 * DAY).toISOString());
  const capCall = h.fetch.calls.find((c) => c.url.endsWith(`/v2/checkout/orders/${PP_ORDER}/capture`));
  assert.equal(capCall.headers.get('paypal-request-id'), `capture-${orderId}`);
  assert.equal(capCall.headers.get('prefer'), 'return=representation');
  assert.equal(h.s.orders.get(orderId).provider_capture_id, PP_CAPTURE);
  const again = await read(await capture(request('POST', `${F}/checkout-capture`, { token: TOKEN_A, body: { orderId } })));
  assert.equal(again.body.status, 'paid');
  assert.equal(h.s.grants, 1);
  // another member cannot touch the order
  assert.equal((await capture(request('POST', `${F}/checkout-capture`, { token: TOKEN_B, body: { orderId } }))).status, 404);
  // a second purchase stacks after the first
  orderId = await paypalOrder(h);
  const second = await read(await capture(request('POST', `${F}/checkout-capture`, { token: TOKEN_A, body: { orderId } })));
  assert.equal(second.body.expiresAt, new Date(NOW.getTime() + 60 * DAY).toISOString());
});

test('checkout-capture refuses mismatched captures and handles declines', async () => {
  let orderId;
  let mode = 'amount';
  const h = harness(paypalRoutes({
    capture: ({ url }) => mode === 'amount' ? { status: 201, json: captureResponse(orderId, { url, value: '0.01' }) }
      : mode === 'currency' ? { status: 201, json: captureResponse(orderId, { url, currency: 'TWD', value: '9.49' }) }
      : mode === 'custom' ? { status: 201, json: captureResponse(orderId, { url, customId: 'MGAAAAAAAAAAAAAAAAAA' }) }
      : mode === 'declined' ? { status: 422, json: { name: 'UNPROCESSABLE_ENTITY', details: [{ issue: 'INSTRUMENT_DECLINED' }] } }
      : { status: 422, json: { name: 'UNPROCESSABLE_ENTITY', details: [{ issue: 'ORDER_ALREADY_CAPTURED' }] } },
    get: ({ url }) => ({ json: captureResponse(orderId, { url }) }),
  }));
  const capture = makeCheckoutCapture(h.deps);
  for (mode of ['amount', 'currency', 'custom']) {
    orderId = await paypalOrder(h);
    const res = await read(await capture(request('POST', `${F}/checkout-capture`, { token: TOKEN_A, body: { orderId } })));
    assert.equal(res.status, 409, mode);
    assert.equal(res.body.status, 'review');
    assert.equal(h.s.orders.get(orderId).status, 'review');
  }
  assert.equal(h.s.grants, 0);
  mode = 'declined';
  orderId = await paypalOrder(h);
  const declined = await read(await capture(request('POST', `${F}/checkout-capture`, { token: TOKEN_A, body: { orderId } })));
  assert.equal(declined.status, 402);
  assert.equal(declined.body.restart, true);
  assert.equal(h.s.orders.get(orderId).status, 'pending');
  mode = 'already';
  const recovered = await read(await capture(request('POST', `${F}/checkout-capture`, { token: TOKEN_A, body: { orderId } })));
  assert.equal(recovered.body.status, 'paid'); // ORDER_ALREADY_CAPTURED → GET order → verified
  assert.equal(h.s.grants, 1);
});

// ----------------------------------------------------------- paypal-webhook
const webhookHeaders = {
  'paypal-auth-algo': 'SHA256withRSA',
  'paypal-cert-url': 'https://api.sandbox.paypal.com/v1/notifications/certs/CERT-1',
  'paypal-transmission-id': 'b1f2c3d4-0000-11ee-8000-000000000001',
  'paypal-transmission-sig': 'c2ln',
  'paypal-transmission-time': '2026-10-15T08:00:00Z',
};

test('paypal-webhook: verified capture grants, refund revokes, duplicates and forgeries ignored', async () => {
  let verdict = 'SUCCESS';
  const h = harness(paypalRoutes({ verify: () => ({ json: { verification_status: verdict } }) }));
  const orderId = await paypalOrder(h);
  const hook = makePayPalWebhook(h.deps);
  const send = (event) => hook(request('POST', `${F}/paypal-webhook`, { origin: null, headers: webhookHeaders, raw: JSON.stringify(event), contentType: 'application/json' })).then(read);
  const completed = {
    id: 'WH-58D329510W468432D-8HN650336L201105X', event_type: 'PAYMENT.CAPTURE.COMPLETED', resource_type: 'capture',
    resource: { id: PP_CAPTURE, status: 'COMPLETED', amount: { currency_code: 'USD', value: '9.49' }, custom_id: orderId, invoice_id: orderId, supplementary_data: { related_ids: { order_id: PP_ORDER } } },
  };
  verdict = 'FAILURE';
  const forged = await send(completed);
  assert.equal(forged.status, 400);
  assert.equal(h.s.grants, 0);
  verdict = 'SUCCESS';
  const ok = await send(completed);
  assert.equal(ok.status, 200);
  assert.equal(ok.body.result, 'paid');
  assert.equal(h.s.orders.get(orderId).status, 'paid');
  const verifyCall = h.fetch.calls.filter((c) => c.url.endsWith('/v1/notifications/verify-webhook-signature')).at(-1);
  assert.equal(JSON.parse(verifyCall.body).webhook_id, ENV.PAYPAL_WEBHOOK_ID);
  assert.equal((await send(completed)).body.duplicate, true);
  assert.equal(h.s.grants, 1);

  const wrongAmount = { ...completed, id: 'WH-WRONG-AMOUNT-1', resource: { ...completed.resource, amount: { currency_code: 'USD', value: '1.00' } } };
  const orderId2 = await paypalOrder(h);
  wrongAmount.resource = { ...wrongAmount.resource, custom_id: orderId2, invoice_id: orderId2 };
  assert.equal((await send(wrongAmount)).body.result, 'mismatch');
  assert.equal(h.s.orders.get(orderId2).status, 'review');

  const refunded = {
    id: 'WH-1GE84257G0350133W-6RW800890C634293G', event_type: 'PAYMENT.CAPTURE.REFUNDED', resource_type: 'refund',
    resource: { id: '1JU08902781691411', status: 'COMPLETED', amount: { currency_code: 'USD', value: '9.49' }, links: [{ rel: 'self', href: `${PP}/v2/payments/refunds/1JU08902781691411` }, { rel: 'up', href: `${PP}/v2/payments/captures/${PP_CAPTURE}` }] },
  };
  assert.equal((await send(refunded)).body.result, 'revoked');
  assert.equal(h.s.orders.get(orderId).status, 'refunded');
  assert.equal(h.s.revokes, 1);
  const reversed = { ...refunded, id: 'WH-REVERSED-0001', event_type: 'PAYMENT.CAPTURE.REVERSED' };
  assert.equal((await send(reversed)).body.result, 'revoked');
  assert.equal(h.s.revokes, 1); // already revoked: idempotent
  assert.equal(h.s.orders.get(orderId).status, 'refunded');
  // a late COMPLETED retry for a refunded order never re-grants
  assert.equal((await send({ ...completed, id: 'WH-LATE-RETRY-0001' })).body.result, 'not_granted_refunded');
  assert.equal(h.s.grants, 1);
});

test('paypal-webhook: CHECKOUT.ORDER.APPROVED captures server-side when the tab was closed', async () => {
  let orderId;
  const h = harness(paypalRoutes({ capture: ({ url }) => ({ status: 201, json: captureResponse(orderId, { url }) }) }));
  orderId = await paypalOrder(h);
  const res = await read(await makePayPalWebhook(h.deps)(request('POST', `${F}/paypal-webhook`, {
    origin: null, headers: webhookHeaders, contentType: 'application/json',
    raw: JSON.stringify({ id: 'WH-APPROVED-0001', event_type: 'CHECKOUT.ORDER.APPROVED', resource: { id: PP_ORDER, status: 'APPROVED' } }),
  })));
  assert.equal(res.body.result, 'approved_paid');
  assert.equal(h.s.orders.get(orderId).status, 'paid');
});

// ------------------------------------------------------------- ecpay-notify
async function ecpayOrder(h) {
  const res = await read(await makeCheckoutCreate(h.deps)(request('POST', `${F}/checkout-create`, { token: TOKEN_A, body: { planId: 'all-30', provider: 'ecpay', termsAccepted: true, termsVersion: 'v12-2026-10' } })));
  return res.body.orderId;
}

async function signed(fields, key = KEY, iv = IV) {
  const out = { ...fields };
  out.CheckMacValue = await ecpay.checkMacValue(out, key, iv);
  return out;
}

function notifyFields(orderId, extra = {}) {
  return {
    MerchantID: '3002607', MerchantTradeNo: orderId, StoreID: '', RtnCode: '1', RtnMsg: '交易成功', TradeNo: '2610151600001234',
    TradeAmt: '299', PaymentDate: '2026/10/15 16:01:02', PaymentType: 'Credit_CreditCard', PaymentTypeChargeFee: '6',
    TradeDate: '2026/10/15 16:00:00', SimulatePaid: '0', CustomField1: '', CustomField2: '', CustomField3: '', CustomField4: '', ...extra,
  };
}

function ecpayRoutes(state) {
  return {
    'POST https://payment-stage.ecpay.com.tw/Cashier/QueryTradeInfo/V5': async ({ body }) => {
      const q = Object.fromEntries(new URLSearchParams(body));
      assert.equal(q.CheckMacValue, await ecpay.checkMacValue(q, KEY, IV), 'QueryTradeInfo request must be signed');
      assert.equal(q.TimeStamp, String(NOW.getTime() / 1000));
      state.queries++;
      const result = await signed({
        MerchantID: '3002607', MerchantTradeNo: q.MerchantTradeNo, StoreID: '', TradeNo: '2610151600001234', TradeAmt: state.amount ?? '299',
        PaymentDate: '2026/10/15 16:01:02', PaymentType: 'Credit_CreditCard', HandlingCharge: '0', PaymentTypeChargeFee: '6',
        TradeDate: '2026/10/15 16:00:00', TradeStatus: state.tradeStatus ?? '1', ItemName: 'MacGyver 工程學院 30 天學習通行證', CustomField1: '', CustomField2: '', CustomField3: '', CustomField4: '',
      }, state.badMac ? 'WRONGKEY00000000' : KEY);
      return { text: new URLSearchParams(result).toString() };
    },
  };
}

test('ecpay-notify: rejects bad MAC / amount / unverified payments; grants once when verified', async () => {
  const state = { queries: 0 };
  const h = harness({ ...paypalRoutes(), ...ecpayRoutes(state) });
  const orderId = await ecpayOrder(h);
  const notify = makeEcpayNotify(h.deps);
  const post = (fields) => notify(request('POST', `${F}/ecpay-notify`, { origin: null, raw: new URLSearchParams(fields).toString() })).then(read);

  const tampered = await signed(notifyFields(orderId));
  tampered.TradeAmt = '1';
  let r = await post(tampered);
  assert.deepEqual([r.status, r.body], [400, '0|ERR']);
  r = await post({ ...(await signed(notifyFields(orderId))), CheckMacValue: 'A'.repeat(64) });
  assert.deepEqual([r.status, r.body], [400, '0|ERR']);
  r = await post(await signed(notifyFields(orderId), 'WRONGKEY00000000'));
  assert.equal(r.body, '0|ERR');
  r = await post(await signed(notifyFields(orderId, { TradeAmt: '300' }))); // correctly signed, wrong amount
  assert.deepEqual([r.status, r.body], [400, '0|ERR']);
  r = await post(await signed(notifyFields('MG0000000000000000FF'))); // unknown order
  assert.equal(r.body, '0|ERR');
  r = await post(await signed(notifyFields(orderId, { MerchantID: '2000132' })));
  assert.equal(r.body, '0|ERR');
  assert.equal((await notify(request('POST', `${F}/ecpay-notify`, { origin: null, raw: '{"a":1}', contentType: 'application/json' }))).status, 415);

  state.tradeStatus = '0'; // ECPay has not confirmed the payment
  r = await post(await signed(notifyFields(orderId)));
  assert.deepEqual([r.status, r.body], [503, '0|ERR']);
  state.tradeStatus = '1';
  state.badMac = true; // forged QueryTradeInfo answer
  r = await post(await signed(notifyFields(orderId)));
  assert.equal(r.body, '0|ERR');
  state.badMac = false;
  state.amount = '298';
  r = await post(await signed(notifyFields(orderId)));
  assert.equal(r.body, '0|ERR');
  state.amount = '299';
  assert.equal(h.s.grants, 0);

  r = await post(await signed(notifyFields(orderId, { SimulatePaid: '1' })));
  assert.deepEqual([r.status, r.body], [200, '1|OK']);
  assert.equal(h.s.grants, 0, 'SimulatePaid never grants');
  r = await post(await signed(notifyFields(orderId, { RtnCode: '10100058', RtnMsg: '付款失敗' })));
  assert.equal(r.body, '1|OK');
  assert.equal(h.s.orders.get(orderId).last_error, 'rtn_10100058');
  assert.equal(h.s.grants, 0);

  const good = await signed(notifyFields(orderId));
  r = await post(good);
  assert.deepEqual([r.status, r.body, r.headers.get('content-type')], [200, '1|OK', 'text/plain; charset=utf-8']);
  assert.equal(h.s.orders.get(orderId).status, 'paid');
  assert.equal(h.s.orders.get(orderId).provider_capture_id, '2610151600001234');
  assert.equal(h.s.grants, 1);
  const queries = state.queries;
  r = await post(good); // ECPay retry of the same notification
  assert.equal(r.body, '1|OK');
  assert.equal(h.s.grants, 1);
  assert.equal(state.queries, queries);

  // the member polls through checkout-capture
  const poll = await read(await makeCheckoutCapture(h.deps)(request('POST', `${F}/checkout-capture`, { token: TOKEN_A, body: { orderId } })));
  assert.deepEqual([poll.status, poll.body.status], [200, 'paid']);
  assert.equal(poll.body.expiresAt, new Date(NOW.getTime() + 30 * DAY).toISOString());
});

// ------------------------------------------------------------ username-login
test('username-login resolves username server-side, rate-limits, generic errors', async () => {
  const session = { access_token: 'at', refresh_token: 'rt', expires_in: 3600, expires_at: 1, token_type: 'bearer', user: { id: USER_A } };
  const gotrue = [];
  const h = harness({
    'POST https://proj.supabase.co/auth/v1/token?grant_type=password': ({ headers, body }) => {
      const b = JSON.parse(body);
      gotrue.push({ apikey: headers.get('apikey'), ...b });
      if (b.email === 'unconfirmed@example.com') return { status: 400, json: { code: 400, error_code: 'email_not_confirmed', msg: 'Email not confirmed' } };
      return b.password === 'correct horse battery staple' ? { json: session } : { status: 400, json: { code: 400, error_code: 'invalid_credentials', msg: 'Invalid login credentials' } };
    },
  });
  const login = makeUsernameLogin(h.deps);
  const call = (body) => login(request('POST', `${F}/username-login`, { body, headers: { 'x-forwarded-for': '203.0.113.9' } })).then(read);
  const ok = await call({ login: 'Alice_01', password: 'correct horse battery staple' });
  assert.equal(ok.status, 200);
  assert.deepEqual(ok.body, session);
  assert.deepEqual(gotrue[0], { apikey: ENV.SUPABASE_ANON_KEY, email: 'alice@example.com', password: 'correct horse battery staple' });
  const byEmail = await call({ login: 'Alice@Example.com', password: 'correct horse battery staple' });
  assert.equal(byEmail.status, 200);
  assert.equal(gotrue[1].email, 'alice@example.com');
  const wrong = await call({ login: 'alice_01', password: 'wrong password 123' });
  const unknown = await call({ login: 'nobody_here', password: 'wrong password 123' });
  assert.deepEqual([wrong.status, wrong.body], [400, { error: 'invalid_credentials', message: 'Incorrect username/email or password.' }]);
  assert.deepEqual(unknown.body, wrong.body, 'unknown usernames are indistinguishable');
  assert.equal(gotrue.length, 3, 'unknown username never reaches GoTrue');
  assert.equal((await call({ login: 'bob', password: 'whatever pass' })).body.error, 'email_not_confirmed');
  assert.equal((await call({ login: 'x y', password: 'p' })).body.error, 'invalid_credentials');
  const fromIp = (ip, body) => login(request('POST', `${F}/username-login`, { body, headers: { 'x-forwarded-for': ip } })).then(read);
  for (let i = 0; i < 10; i++) assert.equal((await fromIp('198.51.100.7', { login: 'alice_01', password: 'guess ' + i })).status, 400);
  const limited = await fromIp('198.51.100.7', { login: 'alice_01', password: 'correct horse battery staple' });
  assert.deepEqual([limited.status, limited.body.error, limited.headers.get('retry-after')], [429, 'rate_limited', '600']);
  assert.equal((await fromIp('198.51.100.8', { login: 'alice_01', password: 'correct horse battery staple' })).status, 200, 'other IPs unaffected');
  assert.ok([...h.s.attempts.keys()].every((k) => /^[0-9a-f]{64}$/.test(k)), 'only hashed keys are stored');
  assert.ok(!JSON.stringify(h.logs).includes('alice@example.com') && !JSON.stringify(h.logs).includes('correct horse'), 'no secrets in logs');
});

// ------------------------------------------------------------ access / fx
test('access returns academy_my_access() plus server time', async () => {
  let orderId;
  const h = harness(paypalRoutes({ capture: ({ url }) => ({ status: 201, json: captureResponse(orderId, { url }) }) }));
  const access = makeAccess(h.deps);
  const before = await read(await access(request('GET', `${F}/access`, { token: TOKEN_A })));
  assert.deepEqual(before.body, { active: false, expiresAt: null, planId: null, serverTime: NOW.toISOString() });
  orderId = await paypalOrder(h);
  await makeCheckoutCapture(h.deps)(request('POST', `${F}/checkout-capture`, { token: TOKEN_A, body: { orderId } }));
  const after = await read(await access(request('POST', `${F}/access`, { token: TOKEN_A })));
  assert.deepEqual(after.body, { active: true, expiresAt: new Date(NOW.getTime() + 30 * DAY).toISOString(), planId: 'all-30', serverTime: NOW.toISOString() });
  assert.equal((await access(request('GET', `${F}/access`))).status, 401);
});

test('fx-refresh requires the cron secret and validates the source', async () => {
  let payload = {
    result: 'success', base_code: 'TWD', time_last_update_unix: NOW.getTime() / 1000 - 3600,
    rates: Object.fromEntries([['TWD', 1], ['USD', 0.0312], ['JPY', 4.6512], ['EUR', 0.02857], ['KRW', 43.1], ['CNY', 'oops']]),
  };
  const h = harness({ [`GET ${FX_SOURCE_URL}`]: () => ({ json: payload }) });
  const fx = makeFxRefresh(h.deps);
  assert.equal((await fx(request('POST', `${F}/fx-refresh`, { origin: null }))).status, 401);
  assert.equal((await fx(request('POST', `${F}/fx-refresh`, { origin: null, headers: { 'x-cron-secret': 'nope' } }))).status, 401);
  const ok = await read(await fx(request('POST', `${F}/fx-refresh`, { origin: null, headers: { 'x-cron-secret': ENV.CRON_SECRET } })));
  assert.equal(ok.status, 200);
  assert.equal(ok.body.updated, 5); // USD JPY EUR KRW + TWD
  assert.ok(ok.body.missing.includes('CNY') && ok.body.missing.includes('GBP'));
  const usd = h.s.fxRows.find((r) => r.currency === 'USD');
  assert.deepEqual(usd, { currency: 'USD', per_twd: '0.0312', source: 'open.er-api.com', updated_at: new Date(NOW.getTime() - 3_600_000).toISOString() });
  payload = { result: 'error', 'error-type': 'unsupported-code' };
  assert.equal((await fx(request('POST', `${F}/fx-refresh`, { origin: null, headers: { 'x-cron-secret': ENV.CRON_SECRET } }))).status, 502);
});

test('helpers: constant-time compare, body limits', async () => {
  assert.equal(http.timingSafeEqual('abc', 'abc'), true);
  assert.equal(http.timingSafeEqual('abc', 'abd'), false);
  assert.equal(http.timingSafeEqual('abc', 'abcd'), false);
  const big = new Request('https://x.test/', { method: 'POST', headers: { 'content-type': 'application/json' }, body: 'x'.repeat(9000) });
  await assert.rejects(http.readJson(big), (e) => e.status === 413);
});

// ------------------------------------------------------------------- run
let failed = 0;
for (const [name, fn] of tests) {
  try {
    await fn();
    console.log(`  ok  ${name}`);
  } catch (error) {
    failed++;
    console.error(`FAIL  ${name}\n${error?.stack ?? error}`);
  }
}
if (failed) {
  console.error(`${failed} payment test(s) failed`);
  process.exit(1);
}
console.log('payments ok');
