// Supabase Edge Function "username-login" (verify_jwt = false). Sign-in with username or email; returns the Supabase Auth session JSON.
// Setup: docs/PAYMENTS_V12_ZH.md. Logic lives in ../_shared (unit-tested with Node).
import { createClient } from 'jsr:@supabase/supabase-js@2';
import { loadConfig } from '../_shared/config.ts';
import { makeUsernameLogin } from '../_shared/handlers/account.ts';
import { storeFromFactory } from '../_shared/store.ts';

const config = loadConfig((name) => Deno.env.get(name));
Deno.serve(makeUsernameLogin({ config, store: storeFromFactory(createClient, config), fetch: fetch.bind(globalThis) }));
