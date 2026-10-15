// PayPal REST helpers (Orders v2 + webhook signature verification). Pure: the
// caller passes `fetch`, so tests run with a fake transport. Card data never
// reaches this server: the PayPal JS SDK (PayPal wallet and the "Debit or Credit
// Card" guest button) collects it on PayPal's side, including 3-D Secure.
import { sameAmount } from './pricing.ts';

export type PayPalEnv = 'sandbox' | 'live';

export const PAYPAL_API: Record<PayPalEnv, string> = {
  sandbox: 'https://api-m.sandbox.paypal.com',
  live: 'https://api-m.paypal.com',
};

export class PayPalError extends Error {
  status: number;
  issue: string;
  debugId: string;
  constructor(status: number, issue: string, message: string, debugId = '') {
    super(message);
    this.status = status;
    this.issue = issue;
    this.debugId = debugId;
  }
}

type Fetch = typeof fetch;
// deno-lint-ignore no-explicit-any
type Json = any;

const tokenCache = new Map<string, { token: string; expiresAt: number }>();

export function clearTokenCache(): void {
  tokenCache.clear();
}

export async function getAccessToken(opts: {
  fetch: Fetch;
  env: PayPalEnv;
  clientId: string;
  clientSecret: string;
  now?: () => number;
}): Promise<string> {
  const now = opts.now ?? Date.now;
  const key = `${opts.env}:${opts.clientId}`;
  const hit = tokenCache.get(key);
  if (hit && hit.expiresAt - 60_000 > now()) return hit.token;
  let res: Response;
  try {
    res = await opts.fetch(`${PAYPAL_API[opts.env]}/v1/oauth2/token`, {
      method: 'POST',
      headers: {
        Authorization: 'Basic ' + btoa(`${opts.clientId}:${opts.clientSecret}`),
        'Content-Type': 'application/x-www-form-urlencoded',
        Accept: 'application/json',
      },
      body: 'grant_type=client_credentials',
      redirect: 'error',
      signal: AbortSignal.timeout(15_000),
    });
  } catch {
    throw new PayPalError(503, 'network', 'PayPal is unreachable.');
  }
  const data: Json = await res.json().catch(() => null);
  if (!res.ok || typeof data?.access_token !== 'string') throw new PayPalError(res.status >= 500 ? 503 : 500, 'auth_failed', 'PayPal authentication failed.');
  const ttl = Number(data.expires_in) > 0 ? Number(data.expires_in) * 1000 : 300_000;
  tokenCache.set(key, { token: data.access_token, expiresAt: now() + ttl });
  return data.access_token;
}

async function call(fetchFn: Fetch, env: PayPalEnv, token: string, method: string, path: string, body?: string, headers: Record<string, string> = {}): Promise<{ status: number; data: Json }> {
  let res: Response;
  try {
    res = await fetchFn(`${PAYPAL_API[env]}${path}`, {
      method,
      headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json', Accept: 'application/json', ...headers },
      body,
      redirect: 'error',
      signal: AbortSignal.timeout(20_000),
    });
  } catch {
    throw new PayPalError(503, 'network', 'PayPal is unreachable.');
  }
  const raw = await res.text();
  let data: Json = null;
  try {
    data = raw ? JSON.parse(raw) : null;
  } catch {
    data = null;
  }
  if (res.status >= 500) throw new PayPalError(503, 'paypal_unavailable', 'PayPal is temporarily unavailable.', data?.debug_id ?? '');
  return { status: res.status, data };
}

export function paypalIssue(data: Json): string {
  const issue = data?.details?.[0]?.issue ?? data?.name ?? '';
  return typeof issue === 'string' ? issue.slice(0, 80) : '';
}

export interface CreateOrderInput {
  orderId: string;
  amount: string;
  currency: string;
  description: string;
  brandName: string;
}

/** Orders v2 body. custom_id and invoice_id carry our order id; invoice_id also blocks duplicate payments. */
export function buildCreateOrderBody(i: CreateOrderInput): Json {
  return {
    intent: 'CAPTURE',
    purchase_units: [{
      reference_id: i.orderId,
      custom_id: i.orderId,
      invoice_id: i.orderId,
      description: i.description.slice(0, 127),
      amount: { currency_code: i.currency, value: i.amount },
    }],
    application_context: {
      brand_name: i.brandName.slice(0, 127),
      shipping_preference: 'NO_SHIPPING',
      user_action: 'PAY_NOW',
    },
  };
}

export async function createOrder(opts: { fetch: Fetch; env: PayPalEnv; accessToken: string } & CreateOrderInput): Promise<{ id: string; status: string }> {
  const { status, data } = await call(opts.fetch, opts.env, opts.accessToken, 'POST', '/v2/checkout/orders', JSON.stringify(buildCreateOrderBody(opts)), {
    'PayPal-Request-Id': `create-${opts.orderId}`,
    Prefer: 'return=minimal',
  });
  if ((status !== 200 && status !== 201) || typeof data?.id !== 'string' || !/^[A-Z0-9]{5,40}$/.test(data.id)) {
    throw new PayPalError(502, paypalIssue(data) || 'create_failed', 'PayPal could not create the order.', data?.debug_id ?? '');
  }
  return { id: data.id, status: String(data.status ?? '') };
}

/** Capture with PayPal-Request-Id idempotency; 4xx responses are returned for the caller to interpret. */
export async function captureOrder(opts: { fetch: Fetch; env: PayPalEnv; accessToken: string; paypalOrderId: string; requestId: string }): Promise<{ status: number; data: Json }> {
  if (!/^[A-Z0-9]{5,40}$/.test(opts.paypalOrderId)) throw new PayPalError(400, 'invalid_order', 'Invalid PayPal order id.');
  return call(opts.fetch, opts.env, opts.accessToken, 'POST', `/v2/checkout/orders/${opts.paypalOrderId}/capture`, undefined, {
    'PayPal-Request-Id': opts.requestId,
    Prefer: 'return=representation',
  });
}

export async function getOrder(opts: { fetch: Fetch; env: PayPalEnv; accessToken: string; paypalOrderId: string }): Promise<Json> {
  if (!/^[A-Z0-9]{5,40}$/.test(opts.paypalOrderId)) throw new PayPalError(400, 'invalid_order', 'Invalid PayPal order id.');
  const { status, data } = await call(opts.fetch, opts.env, opts.accessToken, 'GET', `/v2/checkout/orders/${opts.paypalOrderId}`);
  if (status !== 200) throw new PayPalError(502, paypalIssue(data) || 'get_failed', 'PayPal order lookup failed.', data?.debug_id ?? '');
  return data;
}

export interface ExpectedPayment {
  orderId: string;
  amount: string;
  currency: string;
  paypalOrderId?: string;
}

export type CaptureCheck =
  | { kind: 'completed' | 'pending'; captureId: string }
  | { kind: 'declined' | 'mismatch' | 'incomplete'; reason: string };

/** Verifies one capture object (capture response entry or PAYMENT.CAPTURE.* webhook resource). */
export function checkCaptureResource(capture: Json, expected: ExpectedPayment, customIdFallback?: unknown): CaptureCheck {
  if (!capture || typeof capture !== 'object' || typeof capture.id !== 'string' || !/^[A-Z0-9]{5,40}$/.test(capture.id)) {
    return { kind: 'incomplete', reason: 'no_capture' };
  }
  const currency = capture.amount?.currency_code;
  const value = capture.amount?.value;
  if (currency !== expected.currency) return { kind: 'mismatch', reason: 'currency' };
  if (typeof value !== 'string' || !sameAmount(value, expected.amount, expected.currency)) return { kind: 'mismatch', reason: 'amount' };
  const customId = capture.custom_id ?? customIdFallback;
  if (customId !== expected.orderId) return { kind: 'mismatch', reason: 'custom_id' };
  if (capture.invoice_id !== undefined && capture.invoice_id !== expected.orderId) return { kind: 'mismatch', reason: 'invoice_id' };
  const related = capture.supplementary_data?.related_ids?.order_id;
  if (expected.paypalOrderId && related !== undefined && related !== expected.paypalOrderId) return { kind: 'mismatch', reason: 'paypal_order' };
  if (capture.status === 'COMPLETED') return { kind: 'completed', captureId: capture.id };
  if (capture.status === 'PENDING') return { kind: 'pending', captureId: capture.id };
  if (capture.status === 'DECLINED' || capture.status === 'FAILED') return { kind: 'declined', reason: String(capture.status) };
  return { kind: 'incomplete', reason: 'capture_status' };
}

/** Verifies an Orders v2 capture (or GET order) response against the stored order. */
export function verifyCapture(order: Json, expected: ExpectedPayment): CaptureCheck {
  if (!order || typeof order !== 'object') return { kind: 'incomplete', reason: 'no_order' };
  if (expected.paypalOrderId && order.id !== expected.paypalOrderId) return { kind: 'mismatch', reason: 'paypal_order' };
  const units = order.purchase_units;
  if (!Array.isArray(units) || units.length !== 1) return { kind: 'mismatch', reason: 'purchase_units' };
  const unit = units[0];
  if (unit.custom_id !== undefined && unit.custom_id !== expected.orderId) return { kind: 'mismatch', reason: 'custom_id' };
  if (unit.amount !== undefined && (unit.amount?.currency_code !== expected.currency || !sameAmount(unit.amount?.value, expected.amount, expected.currency))) {
    return { kind: 'mismatch', reason: 'amount' };
  }
  const captures = unit.payments?.captures;
  if (!Array.isArray(captures) || !captures.length) return { kind: 'incomplete', reason: 'no_capture' };
  if (captures.length !== 1) return { kind: 'mismatch', reason: 'multiple_captures' };
  const result = checkCaptureResource(captures[0], expected, unit.custom_id);
  if (result.kind === 'completed' && order.status !== 'COMPLETED') return { kind: 'incomplete', reason: 'order_status' };
  return result;
}

const WEBHOOK_HEADERS = ['paypal-auth-algo', 'paypal-cert-url', 'paypal-transmission-id', 'paypal-transmission-sig', 'paypal-transmission-time'] as const;

/**
 * Request body for POST /v1/notifications/verify-webhook-signature. The raw event
 * body is embedded verbatim (after checking it is a JSON object) so PayPal checks
 * exactly the bytes it signed.
 */
export function buildVerifyWebhookBody(headers: Headers, webhookId: string, rawBody: string): string {
  const v = WEBHOOK_HEADERS.map((h) => headers.get(h) ?? '');
  if (v.some((x) => !x || x.length > 4096)) throw new PayPalError(400, 'missing_headers', 'Missing PayPal transmission headers.');
  if (!/^https:\/\//.test(v[1])) throw new PayPalError(400, 'bad_cert_url', 'Invalid PayPal certificate URL.');
  let parsed: unknown;
  try {
    parsed = JSON.parse(rawBody);
  } catch {
    parsed = null;
  }
  if (!parsed || typeof parsed !== 'object' || Array.isArray(parsed)) throw new PayPalError(400, 'bad_event', 'Webhook body must be a JSON object.');
  const s = JSON.stringify;
  return `{"auth_algo":${s(v[0])},"cert_url":${s(v[1])},"transmission_id":${s(v[2])},"transmission_sig":${s(v[3])},"transmission_time":${s(v[4])},"webhook_id":${s(webhookId)},"webhook_event":${rawBody.trim()}}`;
}

/** True only when PayPal answers verification_status "SUCCESS". */
export async function verifyWebhookSignature(opts: {
  fetch: Fetch;
  env: PayPalEnv;
  accessToken: string;
  webhookId: string;
  headers: Headers;
  rawBody: string;
}): Promise<boolean> {
  const body = buildVerifyWebhookBody(opts.headers, opts.webhookId, opts.rawBody);
  const { status, data } = await call(opts.fetch, opts.env, opts.accessToken, 'POST', '/v1/notifications/verify-webhook-signature', body);
  return status === 200 && data?.verification_status === 'SUCCESS';
}

/** Capture id a refund/reversal resource points to (links rel="up" → /v2/payments/captures/{id}). */
export function relatedCaptureId(resource: Json): string | null {
  const links = Array.isArray(resource?.links) ? resource.links : [];
  for (const link of links) {
    const m = typeof link?.href === 'string' && link.rel === 'up' ? /\/v2\/payments\/captures\/([A-Z0-9]{5,40})$/.exec(link.href) : null;
    if (m) return m[1];
  }
  return null;
}
