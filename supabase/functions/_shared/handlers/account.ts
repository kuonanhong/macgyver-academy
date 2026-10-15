// username-login, access and fx-refresh.
import { clientIp, errorResponse, hmacSha256Hex, HttpError, json, readJson, sleep, timingSafeEqual } from '../http.ts';
import { DEFAULT_RULES, fxCurrencies } from '../pricing.ts';
import type { FxRow } from '../store.ts';
import { browserHandler, type Deps, type Handler, logOf, notConfigured, nowOf, requireUser } from './common.ts';

export const USERNAME = /^[A-Za-z0-9_.-]{3,30}$/;
export const LOGIN_LIMIT = { perIpAndLogin: 10, perLogin: 30, windowSeconds: 900 };

const INVALID = () => new HttpError(400, 'invalid_credentials', 'Incorrect username/email or password.');

// deno-lint-ignore no-explicit-any
type Json = any;

export function makeUsernameLogin(deps: Deps): Handler {
  return browserHandler(deps, 'username_login', ['POST'], async (req) => {
    const cfg = deps.config;
    if (!cfg.anonKey || !cfg.serviceRoleKey || !cfg.supabaseUrl) throw notConfigured(deps, 'supabase');
    const body = await readJson(req, 4096);
    const login = typeof body.login === 'string' ? body.login.trim() : '';
    const password = typeof body.password === 'string' ? body.password : '';
    if (!login || login.length > 254 || !password || password.length > 256) throw INVALID();
    const isEmail = login.includes('@');
    if (isEmail ? !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(login) : !USERNAME.test(login)) throw INVALID();
    const normalized = login.toLowerCase();

    // Hashed (HMAC) keys only: no raw IP or login is stored.
    const ipKey = await hmacSha256Hex(cfg.serviceRoleKey, `mg-login-v1|${clientIp(req)}|${normalized}`);
    const loginKey = await hmacSha256Hex(cfg.serviceRoleKey, `mg-login-v1|*|${normalized}`);
    for (const [key, limit] of [[ipKey, LOGIN_LIMIT.perIpAndLogin], [loginKey, LOGIN_LIMIT.perLogin]] as const) {
      const r = await deps.store.loginAttempt(key, limit, LOGIN_LIMIT.windowSeconds);
      if (!r.allowed) throw new HttpError(429, 'rate_limited', 'Too many sign-in attempts. Please wait and try again.', { retryAfter: Math.max(1, r.retryAfter) });
    }

    const email = isEmail ? normalized : await deps.store.emailForUsername(login);
    if (!email) {
      await sleep(150 + Math.floor(Math.random() * 250)); // blur timing between unknown and wrong-password
      throw INVALID();
    }
    let res: Response;
    try {
      res = await deps.fetch(`${cfg.supabaseUrl}/auth/v1/token?grant_type=password`, {
        method: 'POST',
        headers: { apikey: cfg.anonKey, 'Content-Type': 'application/json', Accept: 'application/json' },
        body: JSON.stringify({ email, password }),
        redirect: 'error',
        signal: AbortSignal.timeout(15_000),
      });
    } catch {
      throw new HttpError(502, 'auth_unavailable', 'Sign-in service is temporarily unavailable.');
    }
    const data: Json = await res.json().catch(() => null);
    if (res.ok && typeof data?.access_token === 'string' && typeof data?.refresh_token === 'string') {
      await deps.store.clearLoginAttempts(ipKey);
      return json(data);
    }
    const code = String(data?.error_code ?? data?.code ?? data?.error ?? '');
    const message = String(data?.msg ?? data?.error_description ?? data?.message ?? '');
    // GoTrue reports an unconfirmed email only after the password matched, so this reveals nothing new.
    if (code === 'email_not_confirmed' || /email not confirmed/i.test(message)) {
      throw new HttpError(400, 'email_not_confirmed', 'Please confirm your email address first (check your inbox).');
    }
    if (res.status === 429) throw new HttpError(429, 'rate_limited', 'Too many sign-in attempts. Please wait and try again.', { retryAfter: 60 });
    if (res.status >= 500) throw new HttpError(502, 'auth_unavailable', 'Sign-in service is temporarily unavailable.');
    throw INVALID();
  });
}

export function makeAccess(deps: Deps): Handler {
  return browserHandler(deps, 'access', ['GET', 'POST'], async (req) => {
    const { token } = await requireUser(req, deps);
    const access = await deps.store.myAccess(token);
    return json({ ...access, serverTime: nowOf(deps).toISOString() });
  });
}

export const FX_SOURCE_URL = 'https://open.er-api.com/v6/latest/TWD';

export function makeFxRefresh(deps: Deps): Handler {
  return async (req) => {
    try {
      if (req.method !== 'POST' && req.method !== 'GET') throw new HttpError(405, 'method_not_allowed', 'Method not allowed.');
      const secret = deps.config.cronSecret;
      if (!secret) throw notConfigured(deps, 'CRON_SECRET');
      if (!timingSafeEqual(req.headers.get('x-cron-secret') ?? '', secret)) throw new HttpError(401, 'unauthorized', 'Unauthorized.');
      const now = nowOf(deps);
      let data: Json;
      try {
        const res = await deps.fetch(FX_SOURCE_URL, { headers: { Accept: 'application/json' }, redirect: 'error', signal: AbortSignal.timeout(15_000) });
        if (!res.ok) throw new Error('status');
        data = await res.json();
      } catch {
        throw new HttpError(502, 'fx_source_unavailable', 'Exchange-rate source is unavailable.');
      }
      if (data?.result !== 'success' || data?.base_code !== 'TWD' || !data.rates || typeof data.rates !== 'object') {
        throw new HttpError(502, 'fx_source_invalid', 'Exchange-rate source returned an invalid payload.');
      }
      const providerMs = Number(data.time_last_update_unix) * 1000;
      // Keep the provider's own timestamp so old data stays "old" and checkout refuses it.
      const known = Number.isFinite(providerMs) && providerMs > 0 && providerMs <= now.getTime() + 3_600_000;
      const updatedAt = (known ? new Date(providerMs) : now).toISOString();
      const stale = known && providerMs < now.getTime() - DEFAULT_RULES.fxMaxAgeDays * 86_400_000;
      const rows: FxRow[] = [];
      const missing: string[] = [];
      for (const currency of fxCurrencies()) {
        const value = data.rates[currency];
        if (typeof value === 'number' && Number.isFinite(value) && value > 0 && value < 1e9) {
          rows.push({ currency, per_twd: String(value), source: 'open.er-api.com', updated_at: updatedAt });
        } else {
          missing.push(currency);
        }
      }
      if (!rows.length) throw new HttpError(502, 'fx_source_invalid', 'No usable exchange rates.');
      rows.push({ currency: 'TWD', per_twd: '1', source: 'fixed', updated_at: now.toISOString() });
      const updated = await deps.store.upsertFxRates(rows);
      logOf(deps)('fx_refreshed', { updated, missing: missing.length, stale });
      return json({ ok: true, updated, missing, stale, providerUpdatedAt: known ? updatedAt : null, source: FX_SOURCE_URL });
    } catch (error) {
      if (!(error instanceof HttpError)) logOf(deps)('fx_refresh_error', { code: 'unexpected' });
      return errorResponse(error);
    }
  };
}
