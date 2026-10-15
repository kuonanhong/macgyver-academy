// Supabase Edge Function "paypal-webhook" (verify_jwt = false). PayPal webhook: verify-webhook-signature, then capture completed / refunded / reversed handling.
// Setup: docs/PAYMENTS_V12_ZH.md. Logic lives in ../_shared (unit-tested with Node).
import { createClient } from 'jsr:@supabase/supabase-js@2';
import { loadConfig } from '../_shared/config.ts';
import { makePayPalWebhook } from '../_shared/handlers/paypal-webhook.ts';
import { storeFromFactory } from '../_shared/store.ts';

const config = loadConfig((name) => Deno.env.get(name));
Deno.serve(makePayPalWebhook({ config, store: storeFromFactory(createClient, config), fetch: fetch.bind(globalThis) }));
