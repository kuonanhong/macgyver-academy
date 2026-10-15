// Supabase Edge Function "checkout-create" (verify_jwt = true). Creates a pending order with a server-computed price and starts PayPal or ECPay checkout.
// Setup: docs/PAYMENTS_V12_ZH.md. Logic lives in ../_shared (unit-tested with Node).
import { createClient } from 'jsr:@supabase/supabase-js@2';
import { loadConfig } from '../_shared/config.ts';
import { makeCheckoutCreate } from '../_shared/handlers/checkout.ts';
import { storeFromFactory } from '../_shared/store.ts';

const config = loadConfig((name) => Deno.env.get(name));
Deno.serve(makeCheckoutCreate({ config, store: storeFromFactory(createClient, config), fetch: fetch.bind(globalThis) }));
