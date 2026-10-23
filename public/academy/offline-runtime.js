/* Browser-local profiles for direct files and static hosts. Cloud authentication
   is a separate optional service installed by services.js. */
(function (window) {
  'use strict';
  const directFile = window.location.protocol === 'file:';
  if (!directFile && window.MG_STATIC_MODE !== true) return;
  const nativeFetch = window.MacGyverNativeFetch || window.fetch.bind(window);

  const memory = new Map();
  let persistent = true, nativeStorage;
  try {
    nativeStorage = window.localStorage;
    const probe = 'mg-offline-storage-probe';
    nativeStorage.setItem(probe, '1'); nativeStorage.removeItem(probe);
    for (let i = 0; i < nativeStorage.length; i++) {
      const key = nativeStorage.key(i); memory.set(key, nativeStorage.getItem(key));
    }
  } catch { persistent = false; }
  function failed() { persistent = false; }
  const safeStorage = {
    get length() { return memory.size; },
    key(index) { return [...memory.keys()][index] ?? null; },
    getItem(key) {
      key = String(key);
      if (persistent) {
        try { const value = nativeStorage.getItem(key); if (value === null) memory.delete(key); else memory.set(key, value); return value; }
        catch { failed(); }
      }
      return memory.get(key) ?? null;
    },
    setItem(key, value) {
      key = String(key); value = String(value); memory.set(key, value);
      if (persistent) try { nativeStorage.setItem(key, value); } catch { failed(); }
    },
    removeItem(key) { key = String(key); memory.delete(key); if (persistent) try { nativeStorage.removeItem(key); } catch { failed(); } },
    clear() { memory.clear(); if (persistent) try { nativeStorage.clear(); } catch { failed(); } }
  };
  // Some browsers deny file:// storage access altogether. The application uses
  // this same safe Storage interface, so even its early language reads can boot.
  try { Object.defineProperty(window, 'localStorage', { configurable: true, get: () => safeStorage }); }
  catch { throw new Error('This browser cannot open the offline storage adapter. Use a current desktop browser or run-local.sh.'); }

  const profileKey = 'mg-offline-profiles-v1';
  const activeKey = 'mg-offline-active-v1';
  const profileId = /^offline-[a-zA-Z0-9-]{6,100}$/;
  const own = (object, key) => Object.prototype.hasOwnProperty.call(object, key);
  const jsonRead = (key, fallback) => { try { return JSON.parse(safeStorage.getItem(key)) ?? fallback; } catch { return fallback; } };
  function profiles() {
    const values = jsonRead(profileKey, []);
    return Array.isArray(values) ? values.filter(p => p && profileId.test(p.id) && typeof p.name === 'string' && p.name.length <= 80).slice(0, 100).map(p => ({ id: p.id, name: p.name, email: typeof p.email === 'string' ? p.email.slice(0,254) : '', username: typeof p.username === 'string' ? p.username.slice(0,30) : '', phone: typeof p.phone === 'string' ? p.phone.slice(0,20) : '', hasPassword: typeof p.passwordHash === 'string' && /^[a-f0-9]{64}$/.test(p.passwordHash) })) : [];
  }
  function activeProfile() {
    const list = profiles();
    return list.find(p => p.id === safeStorage.getItem(activeKey)) || list[0] || null;
  }
  function rawProfile(id) { const list = jsonRead(profileKey, []); return Array.isArray(list) ? list.find(p => p && p.id === id) : null; }
  async function digest(password, salt) {
    const key = await window.crypto.subtle.importKey('raw', new TextEncoder().encode(String(password)), 'PBKDF2', false, ['deriveBits']);
    const bits = await window.crypto.subtle.deriveBits({ name: 'PBKDF2', hash: 'SHA-256', salt: new TextEncoder().encode(salt), iterations: 210000 }, key, 256);
    return [...new Uint8Array(bits)].map(b => b.toString(16).padStart(2, '0')).join('');
  }
  /** V12 local member: username, password, email and mobile phone, all kept in this browser only. */
  async function createMember({ username, password, email, phone, name } = {}) {
    username = String(username || '').trim(); email = String(email || '').trim(); phone = String(phone || '').trim();
    if (!/^[A-Za-z0-9_.-]{3,30}$/.test(username)) throw new Error('帳號需為 3–30 個英數字、底線、點或連字號 / Username: 3–30 letters, digits, _ . -');
    if (typeof password !== 'string' || password.length < 12 || password.length > 128) throw new Error('密碼需 12–128 字元 / Password: 12–128 characters');
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 254) throw new Error('請填寫有效信箱 / Enter a valid email address');
    if (!/^\+[1-9][0-9]{7,14}$/.test(phone)) throw new Error('手機號碼請含國碼 / Mobile number with country code');
    if (profiles().some(p => p.username && p.username.toLowerCase() === username.toLowerCase())) throw new Error('此帳號已存在於本機 / This username already exists on this device');
    if (!window.crypto?.subtle) throw new Error('此瀏覽器不支援安全雜湊 / This browser lacks Web Crypto');
    const salt = [...window.crypto.getRandomValues(new Uint8Array(16))].map(b => b.toString(16).padStart(2, '0')).join('');
    const passwordHash = await digest(password, salt);
    const profile = createProfile(String(name || username).trim().slice(0, 80) || username, email);
    const list = jsonRead(profileKey, []);
    const row = list.find(p => p.id === profile.id);
    Object.assign(row, { username, phone, salt, passwordHash });
    safeStorage.setItem(profileKey, JSON.stringify(list));
    return { ...profile, username, phone, hasPassword: true };
  }
  async function unlockProfile(id, password) {
    const row = rawProfile(id);
    if (!row) throw new Error('找不到本機學習檔案 / Local profile does not exist.');
    if (row.passwordHash) {
      const value = await digest(password, row.salt || '');
      if (value !== row.passwordHash) throw new Error('密碼不正確 / Incorrect password');
    }
    return switchProfile(id, true);
  }
  function switchProfile(id, verified = false) {
    const profile = profiles().find(p => p.id === id);
    if (!profile) throw new Error('找不到本機學習檔案 / Local profile does not exist.');
    if (profile.hasPassword && !verified) throw new Error('此帳號需要密碼 / This account requires its password');
    safeStorage.setItem(activeKey, profile.id); return { ...profile };
  }
  function createProfile(name, email = '') {
    name = typeof name === 'string' ? name.trim().replace(/[\u0000-\u001f\u007f]/g, '') : '';
    if (!name || name.length > 80) throw new Error('名稱需為 1–80 字元 / Use a name of 1–80 characters.');
    email = typeof email === 'string' ? email.trim() : '';
    if (email && (email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email))) throw new Error('請填寫有效信箱或留白 / Use a valid email address or leave it blank.');
    const list = profiles();
    if (list.length >= 100) throw new Error('本機最多 100 個學習檔案 / Maximum 100 local profiles.');
    const random = window.crypto?.randomUUID?.() || `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 14)}`;
    const profile = { id: `offline-${random}`, name, email };
    list.push(profile); safeStorage.setItem(profileKey, JSON.stringify(list));
    return switchProfile(profile.id);
  }
  const firstStaticProfile = !directFile && !activeProfile();
  if (!activeProfile()) createProfile('本機學徒 / Local apprentice');
  function records(id) {
    const value = jsonRead(`mg-offline-records-${id}`, {});
    return value && typeof value === 'object' && !Array.isArray(value) ? value : {};
  }
  const response = (data, status = 200) => new Response(JSON.stringify(data), { status, headers: { 'Content-Type': 'application/json', 'Cache-Control': 'no-store' } });
  function idList(value) {
    if (!Array.isArray(value) || value.length > 5000 || value.some(v => typeof v !== 'string' || !/^[a-zA-Z0-9_.:-]{1,100}$/.test(v))) throw new Error('Invalid progress step list.');
    return [...new Set(value)];
  }
  // V7 static hosting used the guest namespace. Copy valid progress into the
  // first V8 local profile once, retaining the original guest backup untouched.
  if (firstStaticProfile) {
    const legacy=jsonRead('mg-progress-guest',{}), migrated={};
    if(legacy && typeof legacy==='object' && !Array.isArray(legacy))for(const [id,row] of Object.entries(legacy).slice(0,2000)) {
      try {
        if(!/^[a-zA-Z0-9_-]{1,100}$/.test(id)||['__proto__','constructor','prototype'].includes(id)||!row||typeof row.notes!=='string'||row.notes.length>20000)continue;
        migrated[id]={completed:idList(row.completed||[]),assembly:idList(row.assembly||[]),assisted:idList(row.assisted||[]).filter(id=>(row.completed||[]).includes(id)),notes:row.notes,updatedAt:Number.isSafeInteger(row.updatedAt)&&row.updatedAt>=0?row.updatedAt:Date.now()};
      } catch { /* Keep invalid legacy entries in their original backup. */ }
    }
    if(Object.keys(migrated).length)safeStorage.setItem(`mg-offline-records-${activeProfile().id}`,JSON.stringify(migrated));
  }
  window.MacGyverOffline = Object.freeze({
    enabled: true,
    get storageAvailable() { return persistent; },
    listProfiles: profiles, activeProfile, createProfile, switchProfile, createMember, unlockProfile
  });

  window.fetch = async function offlineFetch(input, options = {}) {
    const address = typeof input === 'string' || input instanceof URL ? String(input) : input?.url;
    let url;
    try { url = new URL(address, window.location.href); } catch { return response({ error: 'Invalid offline request.' }, 400); }
    if (directFile && url.protocol !== 'file:') return response({ error: 'Use the explicit AI or external-resource controls to enable network access.' }, 503);
    if (!directFile && url.origin !== window.location.origin) return response({ error: 'Use the explicit AI or external-resource controls to enable network access.' }, 503);
    const method = String(options.method || input?.method || 'GET').toUpperCase();
    const dataName = url.pathname.match(/\/data\/([a-zA-Z0-9_-]+)\.json$/)?.[1];
    if (method === 'GET' && dataName && own(window.MG_DATA || {}, dataName)) return response(window.MG_DATA[dataName]);
    if (directFile && method === 'GET' && dataName && window.MG_LOAD_AUXILIARY) {try{return response(await window.MG_LOAD_AUXILIARY(dataName));}catch{return response({error:'Optional offline data unavailable.'},404);}}
    const api = url.pathname.match(/\/api\/([a-z-]+)$/)?.[1];
    const profile = activeProfile();
    if (api === 'me' && method === 'GET') return response({ user: { ...profile }, aiAvailable: false, authMode: 'offline', deviceOnly: true, storageAvailable: persistent });
    if (api === 'progress' && method === 'GET') return response({ projects: records(profile.id), deviceOnly: true, storageAvailable: persistent });
    if (api === 'progress' && method === 'PUT') {
      try {
        const raw = options.body ?? (typeof input?.text === 'function' ? await input.text() : '');
        if (typeof raw !== 'string' || raw.length > 128 * 1024) return response({ error: 'Progress request is too large.' }, 413);
        const body = JSON.parse(raw);
        if (body?.ownerId && body.ownerId !== profile.id) return response({error:'Learning profile changed. Reload the selected profile before saving.'},401);
        if (!body || typeof body !== 'object' || Array.isArray(body) || typeof body.projectId !== 'string' || !/^[a-zA-Z0-9_-]{1,100}$/.test(body.projectId) || ['__proto__', 'constructor', 'prototype'].includes(body.projectId)) throw new Error('Invalid projectId.');
        if (typeof body.notes !== 'string' || body.notes.length > 20000) throw new Error('Notes must contain at most 20,000 characters.');
        const completed = idList(body.completed), assembly = idList(body.assembly), assisted = idList(body.assisted || []).filter(id=>completed.includes(id));
        const base = body.baseUpdatedAt ?? null;
        if (base !== null && (!Number.isSafeInteger(base) || base < 0)) throw new Error('Invalid baseUpdatedAt.');
        const all = records(profile.id), current = own(all, body.projectId) ? all[body.projectId] : null;
        if ((current && base !== current.updatedAt) || (!current && base !== null)) return response({ error: 'Progress changed in another window', current }, 409);
        if (!current && Object.keys(all).length >= 2000) throw new Error('Maximum 2,000 saved projects per profile.');
        const row = { completed, assembly, assisted, notes: body.notes, updatedAt: Math.max(Date.now(), (current?.updatedAt || 0) + 1) };
        all[body.projectId] = row;
        safeStorage.setItem(`mg-offline-records-${profile.id}`, JSON.stringify(all));
        return response({ projectId: body.projectId, ...row, deviceOnly: true, storageAvailable: persistent });
      } catch (error) { return response({ error: error instanceof SyntaxError ? 'Invalid JSON.' : error.message }, 400); }
    }
    if (api === 'tutor' || api === 'translate') return response({ error: 'Generative AI requires the optional configured server. Offline lesson explanations remain available.' }, 503);
    if (api) return response({ error: 'Direct-file profiles are device records, not password accounts. Use the profile selector.' }, 400);
    if (!directFile && method === 'GET') return nativeFetch(input, options);
    return response({ error: 'This resource is not included in the offline package.' }, 404);
  };
})(window);
