#!/usr/bin/env node
// Server-authenticated owner UI, account switch races and member isolation.
import assert from 'node:assert/strict';
import {configurePaywall, refreshAccess, resetProtectedContent, accessState, hasFullAccess, courseAccessSummary} from '../public/academy/paywall.js';
import {loadBillingConfig, membershipMarkup} from '../public/academy/membership.js';

globalThis.location={protocol:'http:',href:'http://127.0.0.1:8010/'};
const response=data=>({ok:true,json:async()=>data});
const config={mode:'disabled',protected:true,checkoutAvailable:false,freeCourseIds:[],plans:[]};
await loadBillingConfig({fetchImpl:async()=>response(config),force:true});
configurePaywall({config:{paywall:{ownerPreviewOnFile:false}},billing:()=>config,cloud:()=>null});
const course={id:'rail',stepCount:2,stages:[{steps:[{id:'a'}]},{steps:[{id:'b'}]}]};

// A client-side role claim or a cached config entitlement grants nothing.
globalThis.fetch=async()=>response({owner:false,active:false,entitlements:[]});
await refreshAccess({user:{id:'forged',owner:true,role:'owner'}});
assert.equal(hasFullAccess(),false);
assert.equal(accessState().owner,false);

// Only a positive authenticated server result opens all stages without expiry.
globalThis.fetch=async(url,options)=>{
  assert.equal(url,'/api/billing/me');
  assert.equal(options.credentials,'same-origin');
  assert.equal(options.cache,'no-store');
  return response({owner:true,active:true,entitlements:[]});
};
await refreshAccess({user:{id:'real-owner'}});
assert.equal(hasFullAccess(),true);
assert.equal(accessState().expiresAt,null);
assert.match(courseAccessSummary(course),/管理員權限/);
assert.match(membershipMarkup({user:{id:'real-owner',name:'Owner'}}),/管理員無需購買/);
assert.match(membershipMarkup({zh:false,user:{id:'real-owner',name:'Owner'}}),/Owner: no purchase needed/);

// A late private response must not reopen the next user's account after logout.
let resolve;
globalThis.fetch=()=>new Promise(r=>{resolve=r;});
const late=refreshAccess({user:{id:'real-owner'}});
resetProtectedContent();
resolve(response({owner:true,active:true,entitlements:[]}));
await late;
assert.equal(hasFullAccess(),false);
assert.equal(accessState().owner,false);

// Guest and non-200 results fail closed; sandbox passes never unlock live mode.
globalThis.fetch=async()=>({ok:false,status:401});
await refreshAccess({user:{id:'expired'}});
assert.equal(hasFullAccess(),false);
config.mode='live';
globalThis.fetch=async()=>response({owner:false,active:false,entitlements:[{mode:'sandbox',startsAt:0,expiresAt:Date.now()/1000+3600}]});
await refreshAccess({user:{id:'sandbox-user'}});
assert.equal(hasFullAccess(),false);
globalThis.fetch=async()=>response({owner:false,active:true,entitlements:[{mode:'live',startsAt:0,expiresAt:Date.now()/1000+3600}]});
await refreshAccess({user:{id:'paid-member'}});
assert.equal(hasFullAccess(),true);
assert.equal(accessState().owner,false);
await refreshAccess({user:null});
assert.equal(hasFullAccess(),false);
console.log('PASS V16 owner UI: server authority, permanent owner access, disabled purchase, logout race, fail-closed refresh, sandbox/live separation, guest reset.');
