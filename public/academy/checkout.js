/* V12 checkout. Card data is never collected by this site:
 *  - PayPal: the official PayPal JS SDK renders PayPal and "Debit or Credit
 *    Card" buttons; PayPal handles card entry and 3-D Secure. Orders are created
 *    and captured by the owner's Supabase Edge Functions, which verify amount,
 *    currency and payer before granting a pass.
 *  - ECPay (綠界): a signed form is created server-side and the learner pays on
 *    ECPay's hosted page (credit card with 3-D Secure). The pass is granted only
 *    after the server verifies ECPay's notification and queries the trade.
 *  - Python self-hosted backend: existing /api/billing/checkout (ECPay).
 * Payouts (e.g. to the owner's post-office account) are configured in the
 * provider dashboards, never in this code.
 */
export const TERMS_VERSION = 'v12-2026-10';
const PAYPAL_SDK = 'https://www.paypal.com/sdk/js';
const ECPAY_HOSTS = ['payment.ecpay.com.tw', 'payment-stage.ecpay.com.tw'];
let sdkPromise = null, sdkKey = '';

export function paymentSettings(config = globalThis.MG_CONFIG || {}) {
  const p = config.payments || {};
  return {
    paypalClientId: typeof p.paypalClientId === 'string' && /^[A-Za-z0-9_-]{20,120}$/.test(p.paypalClientId) ? p.paypalClientId : '',
    paypalEnv: p.paypalEnv === 'live' ? 'live' : 'sandbox',
    ecpayEnabled: p.ecpayEnabled === true,
    termsUrl: typeof p.termsUrl === 'string' ? p.termsUrl : 'commerce-terms.html'
  };
}
export function checkoutAvailability({cloud = globalThis.MacGyverCloud, billing = {}, config} = {}) {
  const s = paymentSettings(config);
  const cloudReady = !!cloud?.configured;
  return {
    paypal: cloudReady && !!s.paypalClientId,
    ecpay: cloudReady && s.ecpayEnabled,
    server: !!billing?.protected && billing?.checkoutAvailable === true,
    cloudReady, sandbox: s.paypalEnv !== 'live'
  };
}

function loadPayPalSdk(clientId, currency) {
  const key = clientId + ':' + currency;
  if (sdkPromise && sdkKey === key) return sdkPromise;
  document.querySelectorAll('script[data-mg-paypal]').forEach(node => node.remove());
  try { delete globalThis.paypal; } catch { globalThis.paypal = undefined; }
  sdkKey = key;
  sdkPromise = new Promise((resolve, reject) => {
    const script = document.createElement('script');
    const params = new URLSearchParams({'client-id': clientId, currency, intent: 'capture', components: 'buttons,funding-eligibility', 'enable-funding': 'card', 'disable-funding': 'paylater,credit'});
    script.src = PAYPAL_SDK + '?' + params.toString();
    script.dataset.mgPaypal = '1';
    script.async = true;
    script.onload = () => globalThis.paypal ? resolve(globalThis.paypal) : reject(new Error('PayPal SDK unavailable.'));
    script.onerror = () => { sdkPromise = null; reject(new Error('PayPal could not be loaded. Check the network or ad blockers.')); };
    document.head.append(script);
  });
  return sdkPromise;
}

/** Render PayPal + card buttons. Returns a disposer. */
export async function mountPayPalButtons(container, {planId, currency, cloud = globalThis.MacGyverCloud, onPaid = () => {}, onStatus = () => {}, zh = true} = {}) {
  const pick = (a, b) => zh ? a : b;
  const s = paymentSettings();
  if (!container || !s.paypalClientId || !cloud?.callFunction) throw new Error(pick('PayPal 尚未由站長設定。', 'PayPal is not configured by the site owner.'));
  const paypal = await loadPayPalSdk(s.paypalClientId, currency);
  container.replaceChildren();
  let orderId = '';
  const buttons = paypal.Buttons({
    style: {layout: 'vertical', shape: 'rect', label: 'pay', height: 44},
    createOrder: async () => {
      onStatus(pick('正在向伺服器建立訂單並核對金額…', 'Creating the order and verifying the amount on the server…'));
      const result = await cloud.callFunction('checkout-create', {planId, currency, provider: 'paypal', termsAccepted: true, termsVersion: TERMS_VERSION});
      if (!result?.paypalOrderId || !result?.orderId) throw new Error('Unexpected checkout response.');
      orderId = result.orderId;
      onStatus(pick(`伺服器報價：${result.currency} ${result.amount}`, `Server quote: ${result.currency} ${result.amount}`));
      return result.paypalOrderId;
    },
    onApprove: async (data, actions) => {
      onStatus(pick('付款已授權，正在由伺服器確認與入帳…', 'Payment approved; the server is capturing and verifying it…'));
      for (let attempt = 0; attempt < 6; attempt++) {
        let result;
        try { result = await cloud.callFunction('checkout-capture', {orderId}); }
        catch (error) {
          // 402 declined → let the payer choose another card / funding source.
          if (/declin|INSTRUMENT_DECLINED/i.test(String(error.message)) && actions?.restart) { onStatus(pick('卡片被拒絕，請改用其他卡片或付款方式。', 'The card was declined; choose another card or funding source.')); return actions.restart(); }
          throw error;
        }
        if (result?.status === 'paid') { onPaid(result); return; }
        if (result?.status !== 'pending') break;
        await new Promise(r => setTimeout(r, 3000));
      }
      throw new Error(pick('付款尚未完成驗證，請稍後在「我的通行證」重新整理。', 'Payment is not verified yet. Refresh “My passes” later.'));
    },
    onCancel: () => onStatus(pick('已取消付款，未收取任何費用。', 'Payment cancelled; nothing was charged.')),
    onError: error => onStatus(pick('付款失敗：', 'Payment failed: ') + String(error?.message || error))
  });
  if (!buttons.isEligible?.() && buttons.isEligible) throw new Error(pick('此瀏覽器或地區目前無法使用 PayPal。', 'PayPal is not available for this browser or region.'));
  await buttons.render(container);
  return () => { try { buttons.close?.(); } catch {} container.replaceChildren(); };
}

/** Create an ECPay order on the server and submit the signed form. */
export async function startEcpay({planId, cloud = globalThis.MacGyverCloud, zh = true} = {}) {
  const result = await cloud.callFunction('checkout-create', {planId, currency: 'TWD', provider: 'ecpay', termsAccepted: true, termsVersion: TERMS_VERSION});
  submitSignedForm(result, zh);
}
export function submitSignedForm(result, zh = true) {
  let action;
  try { action = new URL(result?.action); } catch { throw new Error(zh ? '付款網址無效。' : 'Invalid payment address.'); }
  if (action.protocol !== 'https:' || !ECPAY_HOSTS.includes(action.hostname) || !result.fields || typeof result.fields !== 'object') throw new Error(zh ? '付款目的地未通過檢查。' : 'Unexpected payment destination.');
  const form = document.createElement('form');
  form.method = 'POST'; form.action = action.href;
  for (const [key, value] of Object.entries(result.fields)) {
    if (!/^[A-Z][A-Za-z0-9]{1,60}$/.test(key) || (typeof value !== 'string' && typeof value !== 'number')) throw new Error('Invalid checkout field.');
    const input = document.createElement('input'); input.type = 'hidden'; input.name = key; input.value = String(value); form.append(input);
  }
  document.body.append(form); form.submit();
}
