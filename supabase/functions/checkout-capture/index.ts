// Supabase Edge Function "checkout-capture" (verify_jwt = true). Captures an approved PayPal order (PayPal-Request-Id idempotency), verifies it and grants the pass; reports ECPay order status for polling.
// Setup: docs/PAYMENTS_V12_ZH.md. Logic lives in ../_shared (unit-tested with Node).
import { createClient } from 'jsr:@supabase/supabase-js@2';
import { loadConfig } from '../_shared/config.ts';
import { makeCheckoutCapture } from '../_shared/handlers/checkout.ts';
import { storeFromFactory } from '../_shared/store.ts';

const config = loadConfig((name) => Deno.env.get(name));
Deno.serve(makeCheckoutCapture({ config, store: storeFromFactory(createClient, config), fetch: fetch.bind(globalThis) }));
