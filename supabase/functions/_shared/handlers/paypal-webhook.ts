// paypal-webhook: every event is verified with PayPal's
// /v1/notifications/verify-webhook-signature (PAYPAL_WEBHOOK_ID) before use, and
// every action is idempotent (event id recorded in payment_events; grant/revoke
// functions are themselves idempotent). 5xx responses make PayPal retry.
import { ORDER_ID } from '../ecpay.ts';
import { errorResponse, HttpError, json, readBody } from '../http.ts';
import { checkCaptureResource, getAccessToken, relatedCaptureId, verifyWebhookSignature } from '../paypal.ts';
import type { OrderRow } from '../store.ts';
import { settlePayPalOrder } from './checkout.ts';
import { type Deps, type Handler, logOf, notConfigured } from './common.ts';

// deno-lint-ignore no-explicit-any
type Json = any;

async function orderFromResource(deps: Deps, resource: Json): Promise<OrderRow | null> {
  for (const candidate of [resource?.custom_id, resource?.invoice_id]) {
    if (typeof candidate === 'string' && ORDER_ID.test(candidate)) {
      const order = await deps.store.getOrder(candidate);
      if (order) return order;
    }
  }
  const related = resource?.supplementary_data?.related_ids?.order_id;
  if (typeof related === 'string' && /^[A-Z0-9]{5,40}$/.test(related)) return deps.store.findOrderBy('paypal', 'provider_order_id', related);
  return null;
}

async function handleEvent(deps: Deps, event: Json): Promise<{ result: string; orderId: string | null }> {
  const pp = deps.config.paypal!;
  const type: string = event.event_type;
  const resource = event.resource ?? {};

  if (type === 'PAYMENT.CAPTURE.COMPLETED') {
    const order = await orderFromResource(deps, resource);
    if (!order || order.provider !== 'paypal') return { result: 'unmatched', orderId: null };
    if (order.env !== pp.env) return { result: 'env_mismatch', orderId: order.id };
    const check = checkCaptureResource(resource, {
      orderId: order.id,
      amount: String(order.amount),
      currency: order.currency,
      paypalOrderId: order.provider_order_id ?? undefined,
    });
    if (check.kind === 'mismatch') {
      await deps.store.updateOrder(order.id, { status: 'review', last_error: `mismatch_${check.reason}` }, ['pending', 'failed']);
      logOf(deps)('paypal_payment_mismatch', { orderId: order.id, reason: check.reason });
      return { result: 'mismatch', orderId: order.id };
    }
    if (check.kind !== 'completed') return { result: 'ignored', orderId: order.id };
    if (order.status === 'review') return { result: 'review', orderId: order.id }; // manual decision only
    if (order.provider_capture_id && order.provider_capture_id !== check.captureId) {
      await deps.store.updateOrder(order.id, { status: 'review', last_error: 'capture_conflict' }, ['pending', 'failed']);
      return { result: 'capture_conflict', orderId: order.id };
    }
    await deps.store.updateOrder(order.id, { provider_capture_id: check.captureId, last_error: null });
    const g = await deps.store.grant(order.id);
    return { result: g.granted ? 'paid' : `not_granted_${g.status}`, orderId: order.id };
  }

  if (type === 'PAYMENT.CAPTURE.REFUNDED' || type === 'PAYMENT.CAPTURE.REVERSED') {
    const captureId = relatedCaptureId(resource);
    const order = (captureId ? await deps.store.findOrderBy('paypal', 'provider_capture_id', captureId) : null) ?? (await orderFromResource(deps, resource));
    if (!order || order.provider !== 'paypal') return { result: 'unmatched', orderId: null };
    const reason = `${type === 'PAYMENT.CAPTURE.REFUNDED' ? 'refunded' : 'reversed'}: paypal ${String(event.id).slice(0, 80)}`;
    const r = await deps.store.revoke(order.id, reason);
    logOf(deps)('order_revoked', { orderId: order.id, provider: 'paypal', status: r.status });
    return { result: 'revoked', orderId: order.id };
  }

  if (type === 'PAYMENT.CAPTURE.DENIED' || type === 'PAYMENT.CAPTURE.DECLINED') {
    const order = await orderFromResource(deps, resource);
    if (!order || order.provider !== 'paypal') return { result: 'unmatched', orderId: null };
    if (order.status === 'paid') {
      await deps.store.revoke(order.id, `reversed: paypal capture denied ${String(event.id).slice(0, 80)}`);
      return { result: 'revoked', orderId: order.id };
    }
    await deps.store.updateOrder(order.id, { status: 'failed', last_error: 'capture_denied' }, ['pending']);
    return { result: 'denied', orderId: order.id };
  }

  if (type === 'CHECKOUT.ORDER.APPROVED') {
    // Safety net when the buyer closed the tab before the browser called checkout-capture.
    const id = resource?.id;
    if (typeof id !== 'string' || !/^[A-Z0-9]{5,40}$/.test(id)) return { result: 'ignored', orderId: null };
    const order = await deps.store.findOrderBy('paypal', 'provider_order_id', id);
    if (!order || order.status !== 'pending') return { result: order ? 'ignored' : 'unmatched', orderId: order?.id ?? null };
    const settled = await settlePayPalOrder(deps, order);
    return { result: `approved_${String(settled.body.status)}`, orderId: order.id };
  }

  return { result: 'ignored', orderId: null };
}

export function makePayPalWebhook(deps: Deps): Handler {
  return async (req) => {
    try {
      if (req.method !== 'POST') throw new HttpError(405, 'method_not_allowed', 'Method not allowed.');
      const pp = deps.config.paypal;
      if (!pp || !pp.webhookId) throw notConfigured(deps, 'paypal-webhook');
      const raw = await readBody(req, 256 * 1024);
      let event: Json;
      try {
        event = JSON.parse(raw);
      } catch {
        throw new HttpError(400, 'invalid_event', 'Invalid event.');
      }
      if (!event || typeof event.id !== 'string' || !/^[A-Za-z0-9-]{5,100}$/.test(event.id) || typeof event.event_type !== 'string') {
        throw new HttpError(400, 'invalid_event', 'Invalid event.');
      }
      if (await deps.store.hasEvent('paypal', event.id)) return json({ ok: true, duplicate: true });

      const accessToken = await getAccessToken({ fetch: deps.fetch, env: pp.env, clientId: pp.clientId, clientSecret: pp.clientSecret });
      const verified = await verifyWebhookSignature({ fetch: deps.fetch, env: pp.env, accessToken, webhookId: pp.webhookId, headers: req.headers, rawBody: raw });
      if (!verified) {
        logOf(deps)('paypal_webhook_bad_signature', { eventType: event.event_type.slice(0, 60) });
        throw new HttpError(400, 'bad_signature', 'Webhook signature verification failed.');
      }

      const outcome = await handleEvent(deps, event);
      await deps.store.recordEvent({
        provider: 'paypal',
        event_key: event.id,
        event_type: event.event_type.slice(0, 80),
        order_id: outcome.orderId,
        result: outcome.result,
        detail: {
          resourceId: typeof event.resource?.id === 'string' ? event.resource.id.slice(0, 64) : null,
          resourceStatus: typeof event.resource?.status === 'string' ? event.resource.status.slice(0, 32) : null,
        },
      });
      logOf(deps)('paypal_webhook', { eventType: event.event_type.slice(0, 60), result: outcome.result, orderId: outcome.orderId });
      return json({ ok: true, result: outcome.result });
    } catch (error) {
      if (!(error instanceof HttpError)) logOf(deps)('paypal_webhook_error', { code: String((error as { issue?: string; code?: string })?.issue ?? (error as { code?: string })?.code ?? 'unexpected').slice(0, 60) });
      return errorResponse(error);
    }
  };
}
