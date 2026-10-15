// ECPay (綠界) AIO V5 credit-card checkout helpers. Pure: Web Crypto + fetch passed in.
// checkMacValue() is byte-for-byte compatible with portable/commerce.py check_mac
// (SHA-256, .NET-style URL encoding, lower-cased before hashing).
import { sha256Hex, timingSafeEqual } from './http.ts';

export type EcpayEnv = 'sandbox' | 'live';

export const ECPAY_HOSTS: Record<EcpayEnv, string> = {
  sandbox: 'https://payment-stage.ecpay.com.tw',
  live: 'https://payment.ecpay.com.tw',
};

/** Public ECPay test merchants: never acceptable for live mode. */
export const ECPAY_TEST_MERCHANTS: readonly string[] = ['2000132', '3002607', '3002599', '3365120'];

export const ORDER_ID = /^MG[0-9A-F]{18}$/;

export class EcpayError extends Error {
  code: string;
  constructor(code: string, message: string) {
    super(message);
    this.code = code;
  }
}

export interface EcpayCredentials {
  merchantId: string;
  hashKey: string;
  hashIV: string;
}

/**
 * .NET HttpUtility.UrlEncode equivalent of Python quote_plus(s, safe="-_.!*()")
 * followed by '~' → %7e and lower-casing: spaces become '+', and only
 * A-Z a-z 0-9 - _ . ! * ( ) stay literal.
 */
export function ecpayUrlEncode(value: string): string {
  return encodeURIComponent(value)
    .replace(/%20/g, '+')
    .replace(/'/g, '%27')
    .replace(/~/g, '%7e')
    .toLowerCase();
}

export function checkMacSource(fields: Record<string, string | number>, hashKey: string, hashIV: string): string {
  const keys = Object.keys(fields)
    .filter((k) => k !== 'CheckMacValue')
    .sort((a, b) => {
      const x = a.toLowerCase();
      const y = b.toLowerCase();
      return x < y ? -1 : x > y ? 1 : 0;
    });
  const raw = keys.map((k) => `${k}=${fields[k]}`).join('&');
  return ecpayUrlEncode(`HashKey=${hashKey}&${raw}&HashIV=${hashIV}`);
}

/** Upper-case hex SHA-256 CheckMacValue (EncryptType=1). */
export async function checkMacValue(fields: Record<string, string | number>, hashKey: string, hashIV: string): Promise<string> {
  return (await sha256Hex(checkMacSource(fields, hashKey, hashIV))).toUpperCase();
}

export async function hasValidMac(fields: Record<string, string>, hashKey: string, hashIV: string): Promise<boolean> {
  const supplied = fields.CheckMacValue ?? '';
  if (!/^[A-Fa-f0-9]{64}$/.test(supplied)) return false;
  return timingSafeEqual(supplied.toUpperCase(), await checkMacValue(fields, hashKey, hashIV));
}

/** "yyyy/MM/dd HH:mm:ss" in Asia/Taipei (UTC+8, no daylight saving). */
export function formatTradeDate(date: Date): string {
  const t = new Date(date.getTime() + 8 * 3_600_000);
  const p = (n: number) => String(n).padStart(2, '0');
  return `${t.getUTCFullYear()}/${p(t.getUTCMonth() + 1)}/${p(t.getUTCDate())} ${p(t.getUTCHours())}:${p(t.getUTCMinutes())}:${p(t.getUTCSeconds())}`;
}

export interface AioOptions {
  env: EcpayEnv;
  merchantId: string;
  orderId: string;
  tradeDate: Date;
  amount: number;
  itemName: string;
  tradeDesc: string;
  returnUrl: string;
  clientBackUrl: string;
}

/** Signed fields for an auto-submitted POST form to ECPay's hosted card page (3-D Secure handled there). */
export async function buildAioFields(o: AioOptions, hashKey: string, hashIV: string): Promise<{ action: string; fields: Record<string, string> }> {
  if (!ORDER_ID.test(o.orderId)) throw new EcpayError('invalid_order', 'Invalid order id.');
  if (!Number.isSafeInteger(o.amount) || o.amount < 1) throw new EcpayError('invalid_amount', 'ECPay amounts are whole TWD.');
  if (!o.itemName || o.itemName.length > 200 || o.itemName.includes('#')) throw new EcpayError('invalid_item', 'Invalid item name.');
  if (!o.tradeDesc || o.tradeDesc.length > 200) throw new EcpayError('invalid_desc', 'Invalid trade description.');
  for (const u of [o.returnUrl, o.clientBackUrl]) {
    if (!/^https:\/\/[^\s]+$/.test(u) || u.length > 200) throw new EcpayError('invalid_url', 'ECPay URLs must be https and at most 200 characters.');
  }
  const fields: Record<string, string> = {
    MerchantID: o.merchantId,
    MerchantTradeNo: o.orderId,
    MerchantTradeDate: formatTradeDate(o.tradeDate),
    PaymentType: 'aio',
    TotalAmount: String(o.amount),
    TradeDesc: o.tradeDesc,
    ItemName: o.itemName,
    ReturnURL: o.returnUrl,
    ClientBackURL: o.clientBackUrl,
    ChoosePayment: 'Credit',
    EncryptType: '1',
    NeedExtraPaidInfo: 'N',
  };
  fields.CheckMacValue = await checkMacValue(fields, hashKey, hashIV);
  return { action: `${ECPAY_HOSTS[o.env]}/Cashier/AioCheckOut/V5`, fields };
}

/** Strict application/x-www-form-urlencoded parser (mirrors commerce.py parse_notification). */
export function parseNotification(raw: string): Record<string, string> {
  if (typeof raw !== 'string' || !raw || raw.length > 32768) throw new EcpayError('invalid_notification', 'Invalid payment notification.');
  const fields: Record<string, string> = Object.create(null);
  const parts = raw.split('&');
  if (parts.length > 100) throw new EcpayError('invalid_notification', 'Too many fields.');
  for (const part of parts) {
    const eq = part.indexOf('=');
    if (eq < 1) throw new EcpayError('invalid_notification', 'Malformed field.');
    let key: string;
    let value: string;
    try {
      key = decodeURIComponent(part.slice(0, eq).replace(/\+/g, ' '));
      value = decodeURIComponent(part.slice(eq + 1).replace(/\+/g, ' '));
    } catch {
      throw new EcpayError('invalid_notification', 'Malformed encoding.');
    }
    if (!/^[A-Za-z][A-Za-z0-9]{0,60}$/.test(key) || value.length > 2000 || key in fields) {
      throw new EcpayError('invalid_notification', 'Invalid or duplicate field.');
    }
    fields[key] = value;
  }
  return { ...fields };
}

export interface EcpayNotification {
  orderId: string;
  amount: number;
  rtnCode: string;
  simulated: boolean;
  tradeNo: string;
  paymentType: string;
  fields: Record<string, string>;
}

/** Signature + identity checks for a ReturnURL notification. Throws EcpayError. */
export async function verifyNotification(fields: Record<string, string>, creds: EcpayCredentials): Promise<EcpayNotification> {
  if (!(await hasValidMac(fields, creds.hashKey, creds.hashIV))) throw new EcpayError('bad_mac', 'Invalid payment signature.');
  if (fields.MerchantID !== creds.merchantId || !ORDER_ID.test(fields.MerchantTradeNo ?? '')) {
    throw new EcpayError('bad_identity', 'Invalid payment merchant or order.');
  }
  const amount = fields.TradeAmt ?? '';
  if (!/^[1-9][0-9]{0,8}$/.test(amount)) throw new EcpayError('bad_amount', 'Invalid payment amount.');
  return {
    orderId: fields.MerchantTradeNo,
    amount: Number(amount),
    rtnCode: fields.RtnCode ?? '',
    // SimulatePaid=1 is ECPay's back-office connectivity probe: never grants access.
    simulated: fields.SimulatePaid !== '0',
    tradeNo: fields.TradeNo ?? '',
    paymentType: fields.PaymentType ?? '',
    fields,
  };
}

export interface StoredOrderForEcpay {
  id: string;
  provider: string;
  currency: string;
  amount_twd: number;
  amount: number | string;
}

/** Checks that a notification matches the stored order (always run, even for failed payments). */
export function matchesOrder(n: EcpayNotification, order: StoredOrderForEcpay | null): boolean {
  return !!order && order.id === n.orderId && order.provider === 'ecpay' && order.currency === 'TWD' &&
    Number(order.amount_twd) === n.amount && Number(order.amount) === n.amount;
}

/**
 * Decision for a successful notification after the independent QueryTradeInfo call:
 * grant only when everything agrees and ECPay reports TradeStatus=1.
 */
export function assessPaid(n: EcpayNotification, order: StoredOrderForEcpay | null, query: Record<string, string> | null): { ok: true } | { ok: false; reason: string } {
  if (n.rtnCode !== '1' || n.simulated) return { ok: false, reason: 'not_paid' };
  if (!matchesOrder(n, order)) return { ok: false, reason: 'order_mismatch' };
  if (!/^[A-Za-z0-9]{1,20}$/.test(n.tradeNo)) return { ok: false, reason: 'bad_trade_no' };
  if (!n.paymentType.startsWith('Credit')) return { ok: false, reason: 'not_credit' };
  if (!query || query.TradeStatus !== '1') return { ok: false, reason: 'query_not_paid' };
  for (const k of ['MerchantID', 'MerchantTradeNo', 'TradeAmt', 'TradeNo', 'PaymentType']) {
    if (query[k] !== n.fields[k]) return { ok: false, reason: 'query_mismatch' };
  }
  return { ok: true };
}

export async function buildQueryFields(creds: EcpayCredentials, orderId: string, now: Date): Promise<Record<string, string>> {
  if (!ORDER_ID.test(orderId)) throw new EcpayError('invalid_order', 'Invalid order id.');
  const fields: Record<string, string> = {
    MerchantID: creds.merchantId,
    MerchantTradeNo: orderId,
    TimeStamp: String(Math.floor(now.getTime() / 1000)),
  };
  fields.CheckMacValue = await checkMacValue(fields, creds.hashKey, creds.hashIV);
  return fields;
}

/** Server-to-server QueryTradeInfo/V5; returns the signature-verified response fields. */
export async function queryTradeInfo(opts: {
  fetch: typeof fetch;
  env: EcpayEnv;
  creds: EcpayCredentials;
  orderId: string;
  now?: Date;
}): Promise<Record<string, string>> {
  const body = new URLSearchParams(await buildQueryFields(opts.creds, opts.orderId, opts.now ?? new Date())).toString();
  let raw: string;
  try {
    const res = await opts.fetch(`${ECPAY_HOSTS[opts.env]}/Cashier/QueryTradeInfo/V5`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body,
      redirect: 'error',
      signal: AbortSignal.timeout(15_000),
    });
    if (!res.ok) throw new Error('status');
    raw = await res.text();
  } catch {
    throw new EcpayError('query_unavailable', 'ECPay order verification is temporarily unavailable.');
  }
  const result = parseNotification(raw.trim());
  if (!(await hasValidMac(result, opts.creds.hashKey, opts.creds.hashIV))) throw new EcpayError('query_bad_mac', 'ECPay verification signature failed.');
  if (result.MerchantID !== opts.creds.merchantId || result.MerchantTradeNo !== opts.orderId) {
    throw new EcpayError('query_identity', 'ECPay verification identity mismatch.');
  }
  return result;
}

/** Stable idempotency key for one notification body. */
export async function notificationKey(fields: Record<string, string>): Promise<string> {
  const sorted = Object.keys(fields).sort().map((k) => [k, fields[k]]);
  return sha256Hex(JSON.stringify(sorted));
}
