// Server-side price computation. Pure: runs unchanged in Deno and Node.
// Rule (pricing.json "rounding"): TWD × rate, rounded UP to the currency's minor
// unit (integer for zeroDecimal currencies, 0.01 otherwise). Exact decimal
// arithmetic with BigInt: no binary floating-point rounding is involved.
import { PRICING_RULES } from './pricing-rules.ts';

export type Provider = 'paypal' | 'ecpay';

export interface Plan {
  id: string;
  title: string;
  titleEn: string;
  amountTwd: number;
  durationDays: number;
}

export interface PricingRules {
  version: number;
  baseCurrency: string;
  plans: Plan[];
  freeStagesPerCourse: number;
  chargeCurrencies: { paypal: string[]; ecpay: string[] };
  fallbackChargeCurrency: string;
  zeroDecimal: string[];
  rounding: string;
  fxMaxAgeDays: number;
}

export const DEFAULT_RULES: PricingRules = PRICING_RULES;
export const PROVIDERS: readonly Provider[] = ['paypal', 'ecpay'];
const ISO = /^[A-Z]{3}$/;

export class PricingError extends Error {
  code: string;
  constructor(code: string, message: string) {
    super(message);
    this.code = code;
  }
}

export function isProvider(value: unknown): value is Provider {
  return value === 'paypal' || value === 'ecpay';
}

export function findPlan(planId: unknown, rules: PricingRules = DEFAULT_RULES): Plan | null {
  return typeof planId === 'string' ? rules.plans.find((p) => p.id === planId) ?? null : null;
}

export function currencyDecimals(currency: string, rules: PricingRules = DEFAULT_RULES): 0 | 2 {
  return rules.zeroDecimal.includes(currency) ? 0 : 2;
}

/** Positive decimal (string or JS number, exponent allowed) as digits / 10^scale. */
export function parseDecimal(value: string | number): { digits: bigint; scale: number } {
  const text = typeof value === 'number' ? (Number.isFinite(value) ? String(value) : '') : String(value).trim();
  const m = /^(\d+)(?:\.(\d+))?(?:[eE]([+-]?\d{1,3}))?$/.exec(text);
  if (!m) throw new PricingError('invalid_decimal', 'Invalid decimal value.');
  const frac = m[2] ?? '';
  let digits = BigInt(m[1] + frac);
  let scale = frac.length - Number(m[3] ?? 0);
  if (scale < 0) {
    digits *= 10n ** BigInt(-scale);
    scale = 0;
  }
  if (scale > 40) throw new PricingError('invalid_decimal', 'Decimal value has too many places.');
  return { digits, scale };
}

/** Exact minor units; throws when the value has more precision than the currency allows. */
export function toMinorUnits(value: string | number, decimals: number): bigint {
  const { digits, scale } = parseDecimal(value);
  if (scale <= decimals) return digits * 10n ** BigInt(decimals - scale);
  const divisor = 10n ** BigInt(scale - decimals);
  if (digits % divisor !== 0n) throw new PricingError('invalid_amount_precision', 'Amount has more precision than the currency allows.');
  return digits / divisor;
}

export function formatMinorUnits(minor: bigint, decimals: number): string {
  if (minor < 0n) throw new PricingError('invalid_amount', 'Negative amount.');
  if (decimals === 0) return minor.toString();
  const unit = 10n ** BigInt(decimals);
  return `${minor / unit}.${(minor % unit).toString().padStart(decimals, '0')}`;
}

/** True when two decimal amounts are exactly equal in the currency's minor units. */
export function sameAmount(a: string | number, b: string | number, currency: string, rules: PricingRules = DEFAULT_RULES): boolean {
  try {
    const d = currencyDecimals(currency, rules);
    return toMinorUnits(a, d) === toMinorUnits(b, d);
  } catch {
    return false;
  }
}

/**
 * Charge amount (provider-ready string such as "9.33" or "280") for a plan priced
 * in TWD. `rates` maps currency → units of that currency per 1 TWD (fx_rates.per_twd).
 */
export function amountFor(
  planTwd: number,
  currency: string,
  rates: Record<string, string | number | undefined>,
  rules: PricingRules = DEFAULT_RULES,
): string {
  if (!Number.isSafeInteger(planTwd) || planTwd < 1) throw new PricingError('invalid_plan_amount', 'Invalid plan amount.');
  if (!ISO.test(currency)) throw new PricingError('invalid_currency', 'Invalid currency code.');
  const decimals = currencyDecimals(currency, rules);
  if (currency === rules.baseCurrency) return formatMinorUnits(BigInt(planTwd) * 10n ** BigInt(decimals), decimals);
  const rate = rates[currency];
  if (rate === undefined || rate === null || rate === '') throw new PricingError('fx_unavailable', `No exchange rate for ${currency}.`);
  const { digits, scale } = parseDecimal(rate);
  if (digits <= 0n) throw new PricingError('fx_unavailable', `Invalid exchange rate for ${currency}.`);
  const numerator = BigInt(planTwd) * digits * 10n ** BigInt(decimals);
  const denominator = 10n ** BigInt(scale);
  const minor = (numerator + denominator - 1n) / denominator; // ceil for positive values
  return formatMinorUnits(minor, decimals);
}

/** Currency actually charged by a provider for the requested currency. */
export function chargeCurrency(provider: Provider, requested: unknown, rules: PricingRules = DEFAULT_RULES): string {
  if (!isProvider(provider)) throw new PricingError('invalid_provider', 'Unknown payment provider.');
  const list = rules.chargeCurrencies[provider];
  const wanted = typeof requested === 'string' ? requested.trim().toUpperCase() : '';
  if (list.includes(wanted)) return wanted;
  if (provider === 'ecpay') return 'TWD';
  return rules.fallbackChargeCurrency;
}

/** fx rates older than pricing.json fxMaxAgeDays must not be used for checkout. */
export function isRateFresh(updatedAt: string | Date | null | undefined, now: Date, rules: PricingRules = DEFAULT_RULES): boolean {
  if (!updatedAt) return false;
  const t = new Date(updatedAt).getTime();
  if (!Number.isFinite(t)) return false;
  return now.getTime() - t <= rules.fxMaxAgeDays * 86_400_000 && t - now.getTime() < 3_600_000;
}

/** Every currency the fx-refresh job keeps: all charge currencies plus common display currencies. */
export const DISPLAY_CURRENCIES: readonly string[] = [
  'CNY', 'KRW', 'MYR', 'IDR', 'VND', 'INR', 'BRL', 'ZAR', 'AED', 'SAR', 'TRY', 'MOP', 'CLP', 'COP', 'ARS', 'PEN', 'EGP', 'NGN', 'KES', 'PKR', 'BDT', 'LKR', 'ISK', 'RON', 'BGN',
];

export function fxCurrencies(rules: PricingRules = DEFAULT_RULES): string[] {
  const all = new Set<string>([...rules.chargeCurrencies.paypal, ...rules.chargeCurrencies.ecpay, ...DISPLAY_CURRENCIES]);
  all.delete(rules.baseCurrency);
  return [...all].sort();
}
