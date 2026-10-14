import {createCloudSync} from './cloud-sync.js';

/* Optional static-host cloud accounts. Local profiles stay useful without a
   backend. A failed cloud save never silently writes into a different profile. */
let initialized = false;
const jsonResponse = (body, status = 200) => new Response(JSON.stringify(body), {status, headers:{'Content-Type':'application/json','Cache-Control':'no-store'}});
export async function initializeServices() {
  if (initialized) return;
  initialized = true;
  if (!window.MacGyverOffline) return;
  const localFetch = window.fetch.bind(window);
  const nativeFetch = window.MacGyverNativeFetch || localFetch;
  let cloudActive = false, cloudOwner = null, authEpoch = 0, authAction = 0;
  const cloud = createCloudSync({config:window.MG_CONFIG || {}, storage:window.localStorage, fetcher:nativeFetch, onAuthChange:session => { const owner=session?.user?.id || null; if(owner!==cloudOwner){cloudOwner=owner;authEpoch++;} }});
  const publicCloud = Object.create(cloud);
  const beginAuthAction=()=>{authEpoch++;return ++authAction;};
  const requireCurrentAction=action=>{if(action!==authAction)throw Object.assign(new Error('Cloud account changed while connecting.'),{code:'auth'});};
  const activateCloud=session=>{cloudOwner=session.user.id;cloudActive=true;delete window.MacGyverCloudStartupError;};
  publicCloud.signIn = async value => {const action=beginAuthAction(),session=await cloud.signIn(value);requireCurrentAction(action);activateCloud(session);return session;};
  publicCloud.signUp = async value => {const action=beginAuthAction(),result=await cloud.signUp(value);requireCurrentAction(action);if(result.user)activateCloud(result);return result;};
  publicCloud.signOut = async () => {beginAuthAction();cloudActive=false;return cloud.signOut();};
  // A retrying getSession only verifies credentials. Switching the learning
  // profile after a failed startup needs this explicit action from the learner.
  publicCloud.resumeSession = async ({expectedUserId}={}) => {
    const action=beginAuthAction(),session=await cloud.getSession();
    requireCurrentAction(action);
    if(!session?.user?.id || (expectedUserId && session.user.id!==expectedUserId))throw Object.assign(new Error('The cloud session changed. Sign in again to continue.'),{code:'auth'});
    activateCloud(session);return session;
  };
  window.MacGyverCloud = publicCloud;
  if (cloud.configured) {
    try {
      const redirect = await cloud.handleRedirect();
      window.MacGyverCloudRecovery = !!redirect.recovery;
      const restored = await cloud.getSession();
      cloudActive = !!restored;
      cloudOwner = restored?.user?.id || null;
    } catch (error) {
      cloudActive = false;
      window.MacGyverCloudStartupError = String(error.message || error);
      // Keep local mode on a fresh startup with an invalid cloud session.
    }
  }
  window.fetch = async function learningServiceFetch(input, options = {}) {
    const address = typeof input === 'string' || input instanceof URL ? String(input) : input?.url;
    let url;
    try {url = new URL(address, window.location.href);} catch {return localFetch(input, options);}
    const ownOrigin = window.location.protocol === 'file:' ? url.protocol === 'file:' : url.origin === window.location.origin;
    const api = ownOrigin && url.pathname.match(/\/api\/(me|progress)$/)?.[1];
    if (!api || !cloudActive) return localFetch(input, options);
    const method = String(options.method || input?.method || 'GET').toUpperCase();
    const requestEpoch=authEpoch;
    const requireSameAccount=()=>{if(requestEpoch!==authEpoch)throw Object.assign(new Error('Cloud account changed while processing this request.'),{code:'auth'});};
    try {
      if (api === 'me' && method === 'GET') {
        const session = await cloud.getSession();
        requireSameAccount();
        return jsonResponse({user:session?.user || null, authMode:'supabase', aiAvailable:false, deviceOnly:false, storageAvailable:window.MacGyverOffline.storageAvailable});
      }
      if (api === 'progress' && method === 'GET') {const projects=await cloud.loadProgress();requireSameAccount();return jsonResponse({projects,deviceOnly:false});}
      if (api === 'progress' && method === 'PUT') {
        const raw = options.body ?? (typeof input?.text === 'function' ? await input.text() : '');
        requireSameAccount();
        if (typeof raw !== 'string' || raw.length > 128*1024) return jsonResponse({error:'Progress request is too large.'},413);
        const body = JSON.parse(raw);
        if (!body || typeof body !== 'object' || Array.isArray(body)) return jsonResponse({error:'Invalid progress.'},400);
        if(body.ownerId!==undefined && body.ownerId!==cloudOwner)return jsonResponse({error:'This progress belongs to another learning profile.'},401);
        const row = await cloud.saveProgress(body.projectId,body,body.baseUpdatedAt ?? null);
        requireSameAccount();
        return jsonResponse({projectId:body.projectId,...row,deviceOnly:false});
      }
      return jsonResponse({error:'Method not allowed.'},405);
    } catch (error) {
      if(requestEpoch!==authEpoch)return jsonResponse({error:'Cloud account changed while processing this request.'},401);
      return jsonResponse({error:String(error.message || error), ...(error.code === 'conflict' ? {current:error.current || null} : {})}, error.code === 'conflict' ? 409 : error.code === 'auth' ? 401 : error.code === 'validation' || error instanceof SyntaxError ? 400 : 503);
    }
  };
}
