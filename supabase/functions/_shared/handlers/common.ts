import type { Config } from '../config.ts';
import { corsHeaders, isOriginAllowed, preflight } from '../cors.ts';
import { bearerToken, consoleLogger, errorResponse, HttpError, type Logger, requireMethod } from '../http.ts';
import { PayPalError } from '../paypal.ts';
import type { Store } from '../store.ts';

export interface Deps {
  config: Config;
  store: Store;
  fetch: typeof fetch;
  now?: () => Date;
  log?: Logger;
}

export type Handler = (req: Request) => Promise<Response>;

export const nowOf = (deps: Deps): Date => (deps.now ? deps.now() : new Date());
export const logOf = (deps: Deps): Logger => deps.log ?? consoleLogger;

function errorCode(error: unknown): string {
  if (error instanceof HttpError) return error.code;
  if (error instanceof PayPalError) return `paypal_${error.issue}`.slice(0, 60);
  const code = (error as { code?: unknown })?.code;
  return typeof code === 'string' ? code.slice(0, 60) : 'unexpected';
}

/** CORS + origin allowlist + method check + uniform JSON errors for browser-facing functions. */
export function browserHandler(deps: Deps, name: string, methods: string[], fn: Handler): Handler {
  const methodList = [...methods, 'OPTIONS'].join(', ');
  return async (req) => {
    const allowed = deps.config.allowedOrigins;
    const pre = preflight(req, allowed, methodList);
    if (pre) return pre;
    const origin = req.headers.get('origin');
    const cors = corsHeaders(origin, allowed, methodList);
    try {
      if (!isOriginAllowed(origin, allowed)) throw new HttpError(403, 'origin_not_allowed', 'This website origin is not allowed.');
      requireMethod(req, ...methods);
      const res = await fn(req);
      const headers = new Headers(res.headers);
      for (const [k, v] of Object.entries(cors)) headers.set(k, v);
      return new Response(res.body, { status: res.status, headers });
    } catch (error) {
      if (!(error instanceof HttpError) || error.status >= 500) logOf(deps)(`${name}_error`, { code: errorCode(error) });
      if (error instanceof PayPalError) {
        return errorResponse(new HttpError(502, 'provider_error', 'PayPal is temporarily unavailable. Please try again.'), cors);
      }
      return errorResponse(error, cors);
    }
  };
}

export async function requireUser(req: Request, deps: Deps): Promise<{ userId: string; emailConfirmed: boolean; token: string }> {
  const token = bearerToken(req);
  if (!token) throw new HttpError(401, 'auth_required', 'Sign in first.');
  const user = await deps.store.getUser(token);
  if (!user) throw new HttpError(401, 'auth_required', 'Your session has expired. Sign in again.');
  return { userId: user.id, emailConfirmed: user.emailConfirmed, token };
}

export function notConfigured(deps: Deps, what: string): HttpError {
  logOf(deps)('not_configured', { what, problems: deps.config.problems.join(',') });
  return new HttpError(503, 'not_configured', 'Payments are not configured yet. Please try again later.');
}
