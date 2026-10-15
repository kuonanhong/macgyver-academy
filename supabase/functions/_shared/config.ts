// Reads Edge Function secrets through an injected getter (index.ts passes
// Deno.env.get), so this module stays free of Deno globals. Never logs values.
import { parseAllowedOrigins } from './cors.ts';
import { ECPAY_TEST_MERCHANTS, type EcpayEnv } from './ecpay.ts';
import type { PayPalEnv } from './paypal.ts';

export interface Config {
  supabaseUrl: string;
  anonKey: string;
  serviceRoleKey: string;
  functionsUrl: string;
  allowedOrigins: string[];
  siteUrl: string;
  termsVersion: string;
  cronSecret: string;
  brandName: string;
  paypal: { env: PayPalEnv; clientId: string; clientSecret: string; webhookId: string } | null;
  ecpay: { env: EcpayEnv; merchantId: string; hashKey: string; hashIV: string } | null;
  /** Names of missing/invalid settings (names only, never values) for 503 diagnostics in logs. */
  problems: string[];
}

function fromKeyList(raw: string | undefined): string {
  // Newer projects also expose SUPABASE_PUBLISHABLE_KEYS / SUPABASE_SECRET_KEYS as JSON {"default": "..."}.
  if (!raw) return '';
  try {
    const parsed = JSON.parse(raw);
    const value = parsed?.default ?? Object.values(parsed ?? {})[0];
    return typeof value === 'string' ? value : '';
  } catch {
    return '';
  }
}

export function loadConfig(get: (name: string) => string | undefined): Config {
  const v = (name: string) => (get(name) ?? '').trim();
  const problems: string[] = [];
  const supabaseUrl = v('SUPABASE_URL').replace(/\/+$/, '');
  if (!/^https?:\/\/[^\s/]+$/.test(supabaseUrl)) problems.push('SUPABASE_URL');
  const anonKey = v('SUPABASE_ANON_KEY') || fromKeyList(get('SUPABASE_PUBLISHABLE_KEYS'));
  const serviceRoleKey = v('SUPABASE_SERVICE_ROLE_KEY') || fromKeyList(get('SUPABASE_SECRET_KEYS'));
  if (!anonKey) problems.push('SUPABASE_ANON_KEY');
  if (!serviceRoleKey) problems.push('SUPABASE_SERVICE_ROLE_KEY');

  let siteUrl = v('SITE_URL');
  try {
    const u = new URL(siteUrl);
    if (u.protocol !== 'https:' || u.search || u.hash) throw new Error();
    siteUrl = u.href.endsWith('/') ? u.href : u.href + '/';
  } catch {
    problems.push('SITE_URL');
    siteUrl = '';
  }

  const ppEnv = v('PAYPAL_ENV');
  let paypal: Config['paypal'] = null;
  if ((ppEnv === 'sandbox' || ppEnv === 'live') && v('PAYPAL_CLIENT_ID') && v('PAYPAL_CLIENT_SECRET')) {
    paypal = { env: ppEnv, clientId: v('PAYPAL_CLIENT_ID'), clientSecret: v('PAYPAL_CLIENT_SECRET'), webhookId: v('PAYPAL_WEBHOOK_ID') };
    if (!paypal.webhookId) problems.push('PAYPAL_WEBHOOK_ID');
  } else if (ppEnv || v('PAYPAL_CLIENT_ID')) {
    problems.push('PAYPAL_ENV/PAYPAL_CLIENT_ID/PAYPAL_CLIENT_SECRET');
  }

  const ecEnv = v('ECPAY_ENV');
  let ecpay: Config['ecpay'] = null;
  const merchantId = v('ECPAY_MERCHANT_ID');
  const hashKey = v('ECPAY_HASH_KEY');
  const hashIV = v('ECPAY_HASH_IV');
  if ((ecEnv === 'sandbox' || ecEnv === 'live') && /^[0-9]{5,10}$/.test(merchantId) && hashKey.length >= 16 && hashIV.length >= 16) {
    if (ecEnv === 'live' && ECPAY_TEST_MERCHANTS.includes(merchantId)) problems.push('ECPAY_MERCHANT_ID (test merchant in live mode)');
    else ecpay = { env: ecEnv, merchantId, hashKey, hashIV };
  } else if (ecEnv || merchantId) {
    problems.push('ECPAY_ENV/ECPAY_MERCHANT_ID/ECPAY_HASH_KEY/ECPAY_HASH_IV');
  }

  const allowedOrigins = parseAllowedOrigins(get('ALLOWED_ORIGINS'));
  if (!allowedOrigins.length) problems.push('ALLOWED_ORIGINS');
  const termsVersion = v('TERMS_VERSION');
  if (!/^[A-Za-z0-9._-]{1,64}$/.test(termsVersion)) problems.push('TERMS_VERSION');
  const cronSecret = v('CRON_SECRET');

  return {
    supabaseUrl,
    anonKey,
    serviceRoleKey,
    functionsUrl: `${supabaseUrl}/functions/v1`,
    allowedOrigins,
    siteUrl,
    termsVersion: /^[A-Za-z0-9._-]{1,64}$/.test(termsVersion) ? termsVersion : '',
    cronSecret: cronSecret.length >= 24 ? cronSecret : '',
    brandName: 'MacGyver Engineering Academy',
    paypal,
    ecpay,
    problems,
  };
}
