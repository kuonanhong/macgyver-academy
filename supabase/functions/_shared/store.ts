// Data access used by the handlers. The interface keeps handlers testable with an
// in-memory fake; createSupabaseStore() implements it with supabase-js clients that
// index.ts creates (service role for server tables, the caller's JWT for RLS reads).
import type { Provider } from './pricing.ts';

export type OrderStatus = 'pending' | 'paid' | 'failed' | 'review' | 'refunded' | 'reversed' | 'revoked';
export const CLOSED_STATUSES: readonly OrderStatus[] = ['refunded', 'reversed', 'revoked'];

export interface OrderRow {
  id: string;
  user_id: string | null;
  plan_id: string;
  provider: Provider;
  env: 'sandbox' | 'live';
  status: OrderStatus;
  currency: string;
  amount: number | string;
  amount_twd: number;
  fx_rate: number | string;
  duration_days: number;
  terms_version: string;
  provider_order_id: string | null;
  provider_capture_id: string | null;
  last_error: string | null;
  created_at?: string;
  paid_at?: string | null;
}

export type NewOrder = Omit<OrderRow, 'provider_order_id' | 'provider_capture_id' | 'last_error' | 'created_at' | 'paid_at'>;

export interface AccessInfo {
  active: boolean;
  expiresAt: string | null;
  planId: string | null;
}

export interface GrantResult {
  granted: boolean;
  status: string;
  orderId: string;
  startsAt?: string;
  expiresAt?: string;
  accessExpiresAt?: string | null;
}

export interface PaymentEvent {
  provider: Provider;
  event_key: string;
  event_type: string;
  order_id: string | null;
  result: string;
  detail: Record<string, string | number | boolean | null>;
}

export interface FxRow {
  currency: string;
  per_twd: string;
  source: string;
  updated_at: string;
}

export interface Store {
  getUser(token: string): Promise<{ id: string; emailConfirmed: boolean } | null>;
  myAccess(token: string): Promise<AccessInfo>;
  getPlanRow(planId: string): Promise<{ id: string; amount_twd: number; duration_days: number; active: boolean } | null>;
  getFxRate(currency: string): Promise<{ per_twd: number | string; updated_at: string } | null>;
  countRecentOrders(userId: string, since: Date): Promise<number>;
  insertOrder(row: NewOrder): Promise<void>;
  getOrder(id: string): Promise<OrderRow | null>;
  findOrderBy(provider: Provider, field: 'provider_order_id' | 'provider_capture_id', value: string): Promise<OrderRow | null>;
  /** Returns false when no row matched (e.g. the status guard failed). */
  updateOrder(id: string, patch: Partial<OrderRow>, onlyIfStatus?: readonly OrderStatus[]): Promise<boolean>;
  grant(orderId: string): Promise<GrantResult>;
  revoke(orderId: string, reason: string): Promise<{ revoked: boolean; status: string }>;
  hasEvent(provider: Provider, key: string): Promise<boolean>;
  /** Inserts once; a duplicate (provider, event_key) is silently ignored. */
  recordEvent(event: PaymentEvent): Promise<void>;
  emailForUsername(username: string): Promise<string | null>;
  loginAttempt(keyHash: string, limit: number, windowSeconds: number): Promise<{ allowed: boolean; retryAfter: number }>;
  clearLoginAttempts(keyHash: string): Promise<void>;
  upsertFxRates(rows: FxRow[]): Promise<number>;
}

// Minimal structural type of the supabase-js client surface we use.
// deno-lint-ignore no-explicit-any
type Client = any;

class DbError extends Error {
  constructor(operation: string, code?: string) {
    // Only the operation and Postgres error code: row data never goes into errors or logs.
    super(`database ${operation} failed${code ? ` (${code})` : ''}`);
  }
}

// deno-lint-ignore no-explicit-any
function check(operation: string, result: { data: any; error: { code?: string } | null }): any {
  if (result.error) throw new DbError(operation, result.error.code);
  return result.data;
}

/** index.ts passes supabase-js createClient (imported from jsr:@supabase/supabase-js@2). */
export function storeFromFactory(
  createClient: (url: string, key: string, options: Record<string, unknown>) => Client,
  config: { supabaseUrl: string; anonKey: string; serviceRoleKey: string },
): Store {
  const auth = { persistSession: false, autoRefreshToken: false, detectSessionInUrl: false };
  // Placeholders keep the worker booting when secrets are missing; handlers then answer 503/500.
  const url = config.supabaseUrl || 'https://not-configured.invalid';
  const admin = createClient(url, config.serviceRoleKey || 'not-configured', { auth });
  return createSupabaseStore(admin, (token) =>
    createClient(url, config.anonKey || 'not-configured', { auth, global: { headers: { Authorization: `Bearer ${token}` } } })
  );
}

export function createSupabaseStore(admin: Client, userClient: (token: string) => Client): Store {
  return {
    async getUser(token) {
      const { data, error } = await admin.auth.getUser(token);
      if (error || !data?.user?.id) return null;
      return { id: data.user.id, emailConfirmed: Boolean(data.user.email_confirmed_at ?? data.user.confirmed_at) };
    },
    async myAccess(token) {
      const data = check('my_access', await userClient(token).rpc('academy_my_access'));
      return { active: data?.active === true, expiresAt: data?.expiresAt ?? null, planId: data?.planId ?? null };
    },
    async getPlanRow(planId) {
      return check('plan', await admin.from('plans').select('id,amount_twd,duration_days,active').eq('id', planId).maybeSingle());
    },
    async getFxRate(currency) {
      return check('fx', await admin.from('fx_rates').select('per_twd,updated_at').eq('currency', currency).maybeSingle());
    },
    async countRecentOrders(userId, since) {
      const r = await admin.from('orders').select('id', { count: 'exact', head: true }).eq('user_id', userId).gte('created_at', since.toISOString());
      if (r.error) throw new DbError('count_orders', r.error.code);
      return r.count ?? 0;
    },
    async insertOrder(row) {
      check('insert_order', await admin.from('orders').insert(row));
    },
    async getOrder(id) {
      return check('order', await admin.from('orders').select('*').eq('id', id).maybeSingle());
    },
    async findOrderBy(provider, field, value) {
      return check('order_by_ref', await admin.from('orders').select('*').eq('provider', provider).eq(field, value).maybeSingle());
    },
    async updateOrder(id, patch, onlyIfStatus) {
      let q = admin.from('orders').update(patch).eq('id', id);
      if (onlyIfStatus?.length) q = q.in('status', onlyIfStatus);
      const rows = check('update_order', await q.select('id'));
      return Array.isArray(rows) && rows.length > 0;
    },
    async grant(orderId) {
      return check('grant', await admin.rpc('academy_grant_entitlement', { p_order_id: orderId }));
    },
    async revoke(orderId, reason) {
      return check('revoke', await admin.rpc('academy_revoke_entitlement', { p_order_id: orderId, p_reason: reason }));
    },
    async hasEvent(provider, key) {
      const row = check('event', await admin.from('payment_events').select('id').eq('provider', provider).eq('event_key', key).maybeSingle());
      return !!row;
    },
    async recordEvent(event) {
      check('record_event', await admin.from('payment_events').upsert(event, { onConflict: 'provider,event_key', ignoreDuplicates: true }));
    },
    async emailForUsername(username) {
      const email = check('login_email', await admin.rpc('academy_login_email', { p_username: username }));
      return typeof email === 'string' && email ? email : null;
    },
    async loginAttempt(keyHash, limit, windowSeconds) {
      const data = check('login_attempt', await admin.rpc('academy_login_attempt', { p_key_hash: keyHash, p_limit: limit, p_window_seconds: windowSeconds }));
      return { allowed: data?.allowed === true, retryAfter: Number(data?.retryAfter) || 0 };
    },
    async clearLoginAttempts(keyHash) {
      check('clear_login', await admin.from('login_attempts').delete().eq('key_hash', keyHash));
    },
    async upsertFxRates(rows) {
      check('fx_upsert', await admin.from('fx_rates').upsert(rows, { onConflict: 'currency' }));
      return rows.length;
    },
  };
}
