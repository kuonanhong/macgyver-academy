/**
 * MacGyver Academy model mirror — Cloudflare Worker.
 *
 * Serves the chunked weights stored in the PRIVATE GitHub repository
 * (e.g. kuonanhong/PRIVATE-MODELS, uploaded by `bash macgyver.sh models`,
 * tools/sync-v13/models_sync.py) to the public website, without ever putting a
 * GitHub token in the browser.
 *
 *   GET /weights-manifest.json        -> <MODEL_PREFIX>weights-manifest.json (schema 1)
 *   GET /parts/<aa>/<sha256>.part      -> <MODEL_PREFIX>parts/… one ≤48 MiB chunk
 *
 * Secrets / vars (wrangler secret put …):
 *   GITHUB_TOKEN    fine-grained PAT: only PRIVATE-MODELS, "Contents: Read-only"
 *   GITHUB_REPO     "kuonanhong/PRIVATE-MODELS"
 *   GITHUB_BRANCH   "main"
 *   ALLOWED_ORIGINS "https://kuonanhong.github.io"
 *   MODEL_PREFIX    "projects/macgyver/"  (V13 shared-repo folder; "" for the V12 root layout)
 *
 * Note: anything this Worker serves can be downloaded by any visitor of the
 * site (the browser must receive the weights to run them). The repository and
 * token stay private; the weights themselves are effectively public.
 */
const PATH = /^\/(weights-manifest\.json|parts\/[A-Za-z0-9._\/-]{1,200})$/;

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    const origin = request.headers.get('Origin') || '';
    const allowed = String(env.ALLOWED_ORIGINS || '').split(',').map(s => s.trim()).filter(Boolean);
    const cors = {
      'Access-Control-Allow-Origin': allowed.includes(origin) ? origin : allowed[0] || 'null',
      'Access-Control-Allow-Methods': 'GET, HEAD, OPTIONS',
      'Access-Control-Max-Age': '86400',
      'Vary': 'Origin'
    };
    if (request.method === 'OPTIONS') return new Response(null, {status: 204, headers: cors});
    if (!['GET', 'HEAD'].includes(request.method)) return new Response('Method not allowed', {status: 405, headers: cors});
    if (origin && !allowed.includes(origin)) return new Response('Origin not allowed', {status: 403, headers: cors});
    const match = url.pathname.match(PATH);
    if (!match || match[1].includes('..')) return new Response('Not found', {status: 404, headers: cors});
    const cache = caches.default;
    const cacheKey = new Request(url.origin + url.pathname, {method: 'GET'});
    let cached = await cache.match(cacheKey);
    if (!cached) {
      const prefix = String(env.MODEL_PREFIX ?? 'projects/macgyver/').replace(/^\/+/, '');
      if (prefix && !/^[A-Za-z0-9._-]+(\/[A-Za-z0-9._-]+)*\/$/.test(prefix)) return new Response('Bad MODEL_PREFIX', {status: 500, headers: cors});
      const api = `https://api.github.com/repos/${env.GITHUB_REPO}/contents/${prefix}${match[1]}?ref=${encodeURIComponent(env.GITHUB_BRANCH || 'main')}`;
      const upstream = await fetch(api, {headers: {
        'Authorization': `Bearer ${env.GITHUB_TOKEN}`,
        'Accept': 'application/vnd.github.raw',
        'User-Agent': 'macgyver-model-mirror',
        'X-GitHub-Api-Version': '2022-11-28'
      }});
      if (!upstream.ok) return new Response('Upstream unavailable', {status: upstream.status === 404 ? 404 : 502, headers: cors});
      const immutable = match[1].startsWith('parts/');
      cached = new Response(upstream.body, {status: 200, headers: {
        'Content-Type': match[1].endsWith('.json') ? 'application/json' : 'application/octet-stream',
        'Cache-Control': immutable ? 'public, max-age=31536000, immutable' : 'public, max-age=300'
      }});
      ctx.waitUntil(cache.put(cacheKey, cached.clone()));
    }
    const headers = new Headers(cached.headers);
    for (const [k, v] of Object.entries(cors)) headers.set(k, v);
    headers.set('X-Content-Type-Options', 'nosniff');
    return new Response(request.method === 'HEAD' ? null : cached.body, {status: 200, headers});
  }
};
