// Supabase Edge Function "access" (verify_jwt = true). Returns the caller's learning-pass status plus server time.
// Setup: docs/PAYMENTS_V12_ZH.md. Logic lives in ../_shared (unit-tested with Node).
import { createClient } from 'jsr:@supabase/supabase-js@2';
import { loadConfig } from '../_shared/config.ts';
import { makeAccess } from '../_shared/handlers/account.ts';
import { storeFromFactory } from '../_shared/store.ts';

const config = loadConfig((name) => Deno.env.get(name));
Deno.serve(makeAccess({ config, store: storeFromFactory(createClient, config), fetch: fetch.bind(globalThis) }));
