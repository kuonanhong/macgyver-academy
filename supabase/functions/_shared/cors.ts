// CORS allowlist from the ALLOWED_ORIGINS secret (comma-separated origins, e.g.
// "https://kuonanhong.github.io,http://localhost:8080"). An origin is scheme +
// host (+ port) only: GitHub Pages project paths such as /macgyver-academy/ are
// not part of the origin. Webhook functions do not use CORS at all.

const ALLOW_HEADERS = 'authorization, x-client-info, apikey, content-type';

export function parseAllowedOrigins(value: string | undefined | null): string[] {
  const out = new Set<string>();
  for (const part of String(value ?? '').split(',')) {
    const raw = part.trim();
    if (!raw) continue;
    try {
      const u = new URL(raw);
      const local = u.hostname === 'localhost' || u.hostname === '127.0.0.1';
      if ((u.protocol === 'https:' || (u.protocol === 'http:' && local)) && !u.username && !u.password) out.add(u.origin);
    } catch {
      // Ignore malformed entries rather than widening access.
    }
  }
  return [...out];
}

/** Requests without an Origin header (curl, server-to-server) are not browser CORS requests. */
export function isOriginAllowed(origin: string | null, allowed: string[]): boolean {
  return origin === null || allowed.includes(origin);
}

export function corsHeaders(origin: string | null, allowed: string[], methods = 'POST, OPTIONS'): Record<string, string> {
  if (!origin || !allowed.includes(origin)) return { Vary: 'Origin' };
  return {
    'Access-Control-Allow-Origin': origin,
    'Access-Control-Allow-Headers': ALLOW_HEADERS,
    'Access-Control-Allow-Methods': methods,
    'Access-Control-Max-Age': '600',
    Vary: 'Origin',
  };
}

/** Answers an OPTIONS preflight (204 when allowed, 403 otherwise); null for other methods. */
export function preflight(req: Request, allowed: string[], methods = 'POST, OPTIONS'): Response | null {
  if (req.method !== 'OPTIONS') return null;
  const origin = req.headers.get('origin');
  const ok = origin !== null && allowed.includes(origin);
  return new Response(null, { status: ok ? 204 : 403, headers: corsHeaders(origin, allowed, methods) });
}
