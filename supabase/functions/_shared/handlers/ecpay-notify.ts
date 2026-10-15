// ecpay-notify (ReturnURL): CheckMacValue + stored-order match + RtnCode=1 +
// server-side QueryTradeInfo (TradeStatus=1, same amount/trade) before granting.
// Answers "1|OK" once processed (including recorded non-payments) and "0|ERR"
// otherwise, so ECPay retries anything that was not safely processed.
import { assessPaid, EcpayError, matchesOrder, notificationKey, parseNotification, queryTradeInfo, verifyNotification } from '../ecpay.ts';
import { HttpError, readBody, text } from '../http.ts';
import { CLOSED_STATUSES } from '../store.ts';
import { type Deps, type Handler, logOf, nowOf } from './common.ts';

export function makeEcpayNotify(deps: Deps): Handler {
  return async (req) => {
    const log = logOf(deps);
    const fail = (status: number, code: string, orderId?: string) => {
      log('ecpay_notify_rejected', { code, orderId: orderId ?? null });
      return text('0|ERR', status);
    };
    try {
      if (req.method !== 'POST') return fail(405, 'method');
      const ec = deps.config.ecpay;
      if (!ec) return fail(503, 'not_configured');
      if (!(req.headers.get('content-type') ?? '').toLowerCase().startsWith('application/x-www-form-urlencoded')) return fail(415, 'content_type');
      const fields = parseNotification(await readBody(req, 32768));
      const n = await verifyNotification(fields, ec);
      const order = await deps.store.getOrder(n.orderId);
      if (!order || !matchesOrder(n, order) || order.env !== ec.env) return fail(400, 'order_mismatch', n.orderId);

      const key = await notificationKey(fields);
      if (await deps.store.hasEvent('ecpay', key)) return text('1|OK');

      let result: string;
      if (n.simulated) {
        result = 'simulated-ignored';
      } else if (n.rtnCode !== '1') {
        await deps.store.updateOrder(order.id, { last_error: `rtn_${n.rtnCode.replace(/[^0-9A-Za-z_-]/g, '').slice(0, 20)}` }, ['pending']);
        result = 'not-paid';
      } else if (CLOSED_STATUSES.includes(order.status)) {
        result = 'revoked-no-grant';
      } else if (order.status === 'review') {
        result = 'review';
      } else {
        if (order.provider_capture_id && order.provider_capture_id !== n.tradeNo) {
          await deps.store.updateOrder(order.id, { status: 'review', last_error: 'trade_conflict' }, ['pending', 'failed']);
          return fail(409, 'trade_conflict', order.id);
        }
        if (order.status !== 'paid') {
          const query = await queryTradeInfo({ fetch: deps.fetch, env: ec.env, creds: ec, orderId: order.id, now: nowOf(deps) });
          const verdict = assessPaid(n, order, query);
          if (!verdict.ok) return fail(verdict.reason === 'query_not_paid' ? 503 : 400, verdict.reason, order.id);
        }
        await deps.store.updateOrder(order.id, { provider_capture_id: n.tradeNo, last_error: null });
        const g = await deps.store.grant(order.id);
        result = g.granted ? 'paid' : `not-granted-${g.status}`;
        log('order_paid', { orderId: order.id, provider: 'ecpay', granted: g.granted });
      }
      await deps.store.recordEvent({
        provider: 'ecpay',
        event_key: key,
        event_type: n.simulated ? 'simulated' : `rtn_${n.rtnCode.slice(0, 20)}`,
        order_id: order.id,
        result,
        detail: { tradeNo: n.tradeNo.slice(0, 20), paymentType: n.paymentType.slice(0, 40), rtnCode: n.rtnCode.slice(0, 20) },
      });
      return text('1|OK');
    } catch (error) {
      if (error instanceof EcpayError) return fail(error.code === 'query_unavailable' ? 503 : 400, error.code);
      if (error instanceof HttpError) return fail(error.status, error.code);
      return fail(500, 'unexpected');
    }
  };
}
