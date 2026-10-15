// HTTP helpers shared by the Edge Functions. Pure: standard Web APIs only
// (Request, Response, crypto.subtle, TextEncoder), so they also run under Node 22.

export class HttpError extends Error {
  status: number;
  code: string;
  extra: Record<string, unknown>;
  constructor(status: number, code: string, message: string, extra: Record<string, unknown> = {}) {
    super(message);
    this.status = status;
    this.code = code;
    this.extra = extra;
  }
}

const BASE_HEADERS: Record<string, string> = {
  'Cache-Control': 'no-store',
  'X-Content-Type-Options': 'nosniff',
};

export function json(body: unknown, status = 200, headers: Record<string, string> = {}): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: { ...BASE_HEADERS, 'Content-Type': 'application/json; charset=utf-8', ...headers },
  });
}

export function text(body: string, status = 200, headers: Record<string, string> = {}): Response {
  return new Response(body, {
    status,
    headers: { ...BASE_HEADERS, 'Content-Type': 'text/plain; charset=utf-8', ...headers },
  });
}

/** JSON error body: {error: code, message, ...extra}. Unknown errors become a generic 500. */
export function errorResponse(error: unknown, headers: Record<string, string> = {}): Response {
  if (error instanceof HttpError) {
    const extra: Record<string, string> = error.status === 429 && typeof error.extra.retryAfter === 'number' ? { 'Retry-After': String(error.extra.retryAfter) } : {};
    return json({ error: error.code, message: error.message, ...error.extra }, error.status, { ...headers, ...extra });
  }
  return json({ error: 'server_error', message: 'Temporary server error; please retry.' }, 500, headers);
}

/** Reads at most maxBytes of the body as UTF-8 text (413 when larger). */
export async function readBody(req: Request, maxBytes: number): Promise<string> {
  const declared = Number(req.headers.get('content-length') ?? '');
  if (Number.isFinite(declared) && declared > maxBytes) throw new HttpError(413, 'payload_too_large', 'Request body is too large.');
  if (!req.body) return '';
  const reader = req.body.getReader();
  const chunks: Uint8Array[] = [];
  let size = 0;
  for (;;) {
    const { done, value } = await reader.read();
    if (done) break;
    size += value.byteLength;
    if (size > maxBytes) {
      await reader.cancel().catch(() => {});
      throw new HttpError(413, 'payload_too_large', 'Request body is too large.');
    }
    chunks.push(value);
  }
  const all = new Uint8Array(size);
  let offset = 0;
  for (const c of chunks) {
    all.set(c, offset);
    offset += c.byteLength;
  }
  try {
    return new TextDecoder('utf-8', { fatal: true }).decode(all);
  } catch {
    throw new HttpError(400, 'invalid_encoding', 'Request body must be UTF-8.');
  }
}

export async function readJson(req: Request, maxBytes = 8192): Promise<Record<string, unknown>> {
  const type = (req.headers.get('content-type') ?? '').toLowerCase();
  if (!type.startsWith('application/json')) throw new HttpError(415, 'unsupported_media_type', 'Send application/json.');
  const raw = await readBody(req, maxBytes);
  let data: unknown;
  try {
    data = JSON.parse(raw);
  } catch {
    throw new HttpError(400, 'invalid_json', 'Invalid JSON body.');
  }
  if (!data || typeof data !== 'object' || Array.isArray(data)) throw new HttpError(400, 'invalid_json', 'JSON body must be an object.');
  return data as Record<string, unknown>;
}

export function requireMethod(req: Request, ...methods: string[]): void {
  if (!methods.includes(req.method)) throw new HttpError(405, 'method_not_allowed', 'Method not allowed.', {});
}

export function bearerToken(req: Request): string | null {
  const m = /^Bearer\s+([A-Za-z0-9._~+/=-]{20,4096})$/.exec(req.headers.get('authorization') ?? '');
  return m ? m[1] : null;
}

/** Best-effort client IP (only used as part of a hashed rate-limit key). */
export function clientIp(req: Request): string {
  const direct = req.headers.get('cf-connecting-ip') ?? req.headers.get('x-real-ip');
  if (direct && direct.length <= 64) return direct.trim();
  const forwarded = (req.headers.get('x-forwarded-for') ?? '').split(',')[0].trim();
  return forwarded && forwarded.length <= 64 ? forwarded : 'unknown';
}

const encoder = new TextEncoder();

function hex(buffer: ArrayBuffer): string {
  return [...new Uint8Array(buffer)].map((b) => b.toString(16).padStart(2, '0')).join('');
}

export async function sha256Hex(value: string): Promise<string> {
  return hex(await crypto.subtle.digest('SHA-256', encoder.encode(value)));
}

export async function hmacSha256Hex(key: string, value: string): Promise<string> {
  const k = await crypto.subtle.importKey('raw', encoder.encode(key), { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  return hex(await crypto.subtle.sign('HMAC', k, encoder.encode(value)));
}

/** Constant-time comparison for secrets and MAC values (length leak only). */
export function timingSafeEqual(a: string, b: string): boolean {
  const x = encoder.encode(a);
  const y = encoder.encode(b);
  let diff = x.length ^ y.length;
  const n = Math.max(x.length, y.length);
  for (let i = 0; i < n; i++) diff |= (x[i] ?? 0) ^ (y[i] ?? 0);
  return diff === 0;
}

export function randomHex(bytes: number): string {
  const b = new Uint8Array(bytes);
  crypto.getRandomValues(b);
  return [...b].map((v) => v.toString(16).padStart(2, '0')).join('');
}

/** Structured logs. Callers pass only IDs and codes: never emails, phones, passwords, tokens, card data or secrets. */
export type LogFields = Record<string, string | number | boolean | null | undefined>;
export type Logger = (event: string, fields?: LogFields) => void;

export const consoleLogger: Logger = (event, fields = {}) => {
  console.log(JSON.stringify({ event, ...fields }));
};

export const sleep = (ms: number) => new Promise<void>((resolve) => setTimeout(resolve, ms));
