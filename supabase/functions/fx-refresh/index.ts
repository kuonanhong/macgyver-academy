// Supabase Edge Function "fx-refresh" (verify_jwt = false). Weekly exchange-rate refresh; requires the x-cron-secret header.
// Setup: docs/PAYMENTS_V12_ZH.md. Logic lives in ../_shared (unit-tested with Node).
import { createClient } from 'jsr:@supabase/supabase-js@2';
import { loadConfig } from '../_shared/config.ts';
import { makeFxRefresh } from '../_shared/handlers/account.ts';
import { storeFromFactory } from '../_shared/store.ts';

const config = loadConfig((name) => Deno.env.get(name));
Deno.serve(makeFxRefresh({ config, store: storeFromFactory(createClient, config), fetch: fetch.bind(globalThis) }));
