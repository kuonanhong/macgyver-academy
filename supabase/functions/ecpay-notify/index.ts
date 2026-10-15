// Supabase Edge Function "ecpay-notify" (verify_jwt = false). ECPay ReturnURL: CheckMacValue + QueryTradeInfo before granting; answers 1|OK or 0|ERR.
// Setup: docs/PAYMENTS_V12_ZH.md. Logic lives in ../_shared (unit-tested with Node).
import { createClient } from 'jsr:@supabase/supabase-js@2';
import { loadConfig } from '../_shared/config.ts';
import { makeEcpayNotify } from '../_shared/handlers/ecpay-notify.ts';
import { storeFromFactory } from '../_shared/store.ts';

const config = loadConfig((name) => Deno.env.get(name));
Deno.serve(makeEcpayNotify({ config, store: storeFromFactory(createClient, config), fetch: fetch.bind(globalThis) }));
