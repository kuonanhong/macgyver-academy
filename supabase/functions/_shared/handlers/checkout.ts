// checkout-create and checkout-capture. Prices are computed here from the bundled
// pricing.json copy; the client's amount (if any) is ignored.
import { buildAioFields, ORDER_ID } from '../ecpay.ts';
import { HttpError, json, randomHex, readJson } from '../http.ts';
import { captureOrder, createOrder, getAccessToken, getOrder, paypalIssue, verifyCapture } from '../paypal.ts';
import { amountFor, chargeCurrency, findPlan, isProvider, isRateFresh, PricingError } from '../pricing.ts';
import { CLOSED_STATUSES, type OrderRow } from '../store.ts';
import { browserHandler, type Deps, type Handler, logOf, notConfigured, nowOf, requireUser } from './common.ts';

const ORDERS_PER_HOUR = 10;

export function makeCheckoutCreate(deps: Deps): Handler {
  return browserHandler(deps, 'checkout_create', ['POST'], async (req) => {
    const cfg = deps.config;
    const { userId, emailConfirmed } = await requireUser(req, deps);
    if (!emailConfirmed) throw new HttpError(403, 'email_not_confirmed', 'Verify your email address before buying a pass.');
    const body = await readJson(req);
    const plan = findPlan(body.planId);
    if (!plan) throw new HttpError(400, 'invalid_plan', 'Choose a valid plan.');
    if (!isProvider(body.provider)) throw new HttpError(400, 'invalid_provider', 'Choose PayPal or ECPay.');
    const provider = body.provider;
    if (body.termsAccepted !== true) throw new HttpError(400, 'terms_required', 'Accept the purchase terms first.');
    if (!cfg.termsVersion || !cfg.siteUrl) throw notConfigured(deps, 'terms/site');
    if (body.termsVersion !== cfg.termsVersion) {
      throw new HttpError(409, 'terms_outdated', 'The purchase terms were updated. Please review them again.', { termsVersion: cfg.termsVersion });
    }
    if (body.currency !== undefined && body.currency !== null && (typeof body.currency !== 'string' || !/^[A-Za-z]{3}$/.test(body.currency))) {
      throw new HttpError(400, 'invalid_currency', 'Invalid currency code.');
    }
    if (provider === 'paypal' && !cfg.paypal) throw notConfigured(deps, 'paypal');
    if (provider === 'ecpay' && !cfg.ecpay) throw notConfigured(deps, 'ecpay');

    // The database plan row must agree with pricing.json (fail closed if the owner forgot to sync).
    const row = await deps.store.getPlanRow(plan.id);
    if (!row || !row.active || row.amount_twd !== plan.amountTwd || row.duration_days !== plan.durationDays) {
      logOf(deps)('pricing_mismatch', { planId: plan.id });
      throw new HttpError(503, 'pricing_mismatch', 'This plan is temporarily unavailable.');
    }

    const now = nowOf(deps);
    const currency = chargeCurrency(provider, body.currency ?? 'TWD');
    let rate = '1';
    if (currency !== 'TWD') {
      const fx = await deps.store.getFxRate(currency);
      if (!fx || !isRateFresh(fx.updated_at, now)) {
        throw new HttpError(503, 'fx_unavailable', `Exchange rate for ${currency} is unavailable. Please pay in TWD.`, { fallbackCurrency: 'TWD' });
      }
      rate = String(fx.per_twd);
    }
    let amount: string;
    try {
      amount = amountFor(plan.amountTwd, currency, { [currency]: rate });
    } catch (e) {
      if (e instanceof PricingError) throw new HttpError(503, 'fx_unavailable', 'Price could not be computed. Please pay in TWD.', { fallbackCurrency: 'TWD' });
      throw e;
    }

    if ((await deps.store.countRecentOrders(userId, new Date(now.getTime() - 3_600_000))) >= ORDERS_PER_HOUR) {
      throw new HttpError(429, 'too_many_orders', 'Too many checkout attempts. Please try again later.', { retryAfter: 900 });
    }

    const orderId = 'MG' + randomHex(9).toUpperCase();
    const env = provider === 'paypal' ? cfg.paypal!.env : cfg.ecpay!.env;
    await deps.store.insertOrder({
      id: orderId,
      user_id: userId,
      plan_id: plan.id,
      provider,
      env,
      status: 'pending',
      currency,
      amount,
      amount_twd: plan.amountTwd,
      fx_rate: rate,
      duration_days: plan.durationDays,
      terms_version: cfg.termsVersion,
    });
    logOf(deps)('order_created', { orderId, provider, currency, planId: plan.id, env });

    if (provider === 'paypal') {
      const pp = cfg.paypal!;
      let paypalOrderId: string;
      try {
        const accessToken = await getAccessToken({ fetch: deps.fetch, env: pp.env, clientId: pp.clientId, clientSecret: pp.clientSecret });
        paypalOrderId = (await createOrder({
          fetch: deps.fetch,
          env: pp.env,
          accessToken,
          orderId,
          amount,
          currency,
          description: `${plan.titleEn} - ${cfg.brandName}`,
          brandName: cfg.brandName,
        })).id;
      } catch (e) {
        logOf(deps)('paypal_create_failed', { orderId, issue: (e as { issue?: string }).issue ?? 'unknown' });
        await deps.store.updateOrder(orderId, { status: 'failed', last_error: 'paypal_create_failed' }, ['pending']);
        throw new HttpError(502, 'provider_error', 'PayPal could not start the payment. Please try again.');
      }
      await deps.store.updateOrder(orderId, { provider_order_id: paypalOrderId });
      return json({ orderId, provider: 'paypal', amount, currency, paypalOrderId, planId: plan.id, durationDays: plan.durationDays });
    }

    const ec = cfg.ecpay!;
    const { action, fields } = await buildAioFields({
      env: ec.env,
      merchantId: ec.merchantId,
      orderId,
      tradeDate: now,
      amount: Number(amount),
      itemName: `MacGyver 工程學院 ${plan.title}`,
      tradeDesc: 'MacGyver Engineering Academy learning pass',
      returnUrl: `${cfg.functionsUrl}/ecpay-notify`,
      clientBackUrl: `${cfg.siteUrl}?payment=ecpay&order=${orderId}`,
    }, ec.hashKey, ec.hashIV);
    return json({ orderId, provider: 'ecpay', action, fields, amount, currency: 'TWD', planId: plan.id, durationDays: plan.durationDays });
  });
}

export interface SettleResult {
  httpStatus: number;
  body: Record<string, unknown>;
}

function amountString(order: OrderRow): string {
  return String(order.amount);
}

/** Captures (idempotently) and verifies a PayPal order, then grants. Shared by checkout-capture and the webhook. */
export async function settlePayPalOrder(deps: Deps, order: OrderRow): Promise<SettleResult> {
  const log = logOf(deps);
  if (order.status === 'paid') {
    const g = await deps.store.grant(order.id);
    return { httpStatus: 200, body: { status: 'paid', orderId: order.id, expiresAt: g.accessExpiresAt ?? g.expiresAt ?? null } };
  }
  if (CLOSED_STATUSES.includes(order.status) || order.status === 'review') {
    return { httpStatus: 409, body: { status: order.status, orderId: order.id, error: 'order_closed' } };
  }
  const pp = deps.config.paypal;
  if (!pp) throw notConfigured(deps, 'paypal');
  if (order.env !== pp.env || !order.provider_order_id) {
    return { httpStatus: 409, body: { status: 'failed', orderId: order.id, error: 'order_not_capturable' } };
  }
  const expected = { orderId: order.id, amount: amountString(order), currency: order.currency, paypalOrderId: order.provider_order_id };
  const accessToken = await getAccessToken({ fetch: deps.fetch, env: pp.env, clientId: pp.clientId, clientSecret: pp.clientSecret });
  const cap = await captureOrder({ fetch: deps.fetch, env: pp.env, accessToken, paypalOrderId: order.provider_order_id, requestId: `capture-${order.id}` });
  let data = cap.data;
  if (cap.status !== 200 && cap.status !== 201) {
    const issue = paypalIssue(cap.data);
    if (issue === 'ORDER_ALREADY_CAPTURED') {
      data = await getOrder({ fetch: deps.fetch, env: pp.env, accessToken, paypalOrderId: order.provider_order_id });
    } else if (issue === 'INSTRUMENT_DECLINED') {
      return { httpStatus: 402, body: { status: 'declined', orderId: order.id, error: 'instrument_declined', restart: true } };
    } else if (issue === 'ORDER_NOT_APPROVED' || issue === 'PAYER_ACTION_REQUIRED') {
      return { httpStatus: 409, body: { status: 'not_approved', orderId: order.id, error: 'not_approved' } };
    } else {
      log('paypal_capture_rejected', { orderId: order.id, status: cap.status, issue });
      if (cap.status === 404 || issue === 'ORDER_EXPIRED' || issue === 'RESOURCE_NOT_FOUND') {
        await deps.store.updateOrder(order.id, { status: 'failed', last_error: 'paypal_order_unavailable' }, ['pending']);
      }
      return { httpStatus: 402, body: { status: 'declined', orderId: order.id, error: 'capture_failed' } };
    }
  }
  const check = verifyCapture(data, expected);
  switch (check.kind) {
    case 'completed': {
      if (order.provider_capture_id && order.provider_capture_id !== check.captureId) {
        await deps.store.updateOrder(order.id, { status: 'review', last_error: 'capture_conflict' }, ['pending', 'failed']);
        log('paypal_capture_conflict', { orderId: order.id });
        return { httpStatus: 409, body: { status: 'review', orderId: order.id, error: 'payment_review' } };
      }
      await deps.store.updateOrder(order.id, { provider_capture_id: check.captureId, last_error: null });
      const g = await deps.store.grant(order.id);
      log('order_paid', { orderId: order.id, provider: 'paypal', granted: g.granted });
      if (!g.granted) return { httpStatus: 409, body: { status: g.status, orderId: order.id, error: 'order_closed' } };
      return { httpStatus: 200, body: { status: 'paid', orderId: order.id, expiresAt: g.accessExpiresAt ?? g.expiresAt ?? null } };
    }
    case 'pending':
      await deps.store.updateOrder(order.id, { provider_capture_id: check.captureId, last_error: 'capture_pending' }, ['pending']);
      return { httpStatus: 202, body: { status: 'pending', orderId: order.id, expiresAt: null } };
    case 'declined':
      await deps.store.updateOrder(order.id, { last_error: 'capture_declined' }, ['pending']);
      return { httpStatus: 402, body: { status: 'declined', orderId: order.id, error: 'instrument_declined', restart: true } };
    case 'mismatch':
      await deps.store.updateOrder(order.id, { status: 'review', last_error: `mismatch_${check.reason}` }, ['pending', 'failed']);
      log('paypal_payment_mismatch', { orderId: order.id, reason: check.reason });
      return { httpStatus: 409, body: { status: 'review', orderId: order.id, error: 'payment_review' } };
    default:
      log('paypal_capture_incomplete', { orderId: order.id, reason: check.reason });
      return { httpStatus: 202, body: { status: 'pending', orderId: order.id, expiresAt: null } };
  }
}

export function makeCheckoutCapture(deps: Deps): Handler {
  return browserHandler(deps, 'checkout_capture', ['POST'], async (req) => {
    const { userId, token } = await requireUser(req, deps);
    const body = await readJson(req);
    if (typeof body.orderId !== 'string' || !ORDER_ID.test(body.orderId)) throw new HttpError(400, 'invalid_order', 'Invalid order id.');
    const order = await deps.store.getOrder(body.orderId);
    if (!order || order.user_id !== userId) throw new HttpError(404, 'order_not_found', 'Order not found.');
    if (order.provider === 'ecpay') {
      // ECPay is confirmed only by the server-to-server notification; this only reports status for polling.
      const access = order.status === 'paid' ? await deps.store.myAccess(token) : null;
      return json({ status: order.status, orderId: order.id, expiresAt: access?.expiresAt ?? null }, order.status === 'pending' ? 202 : 200);
    }
    const result = await settlePayPalOrder(deps, order);
    return json(result.body, result.httpStatus);
  });
}
