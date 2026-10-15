-- MacGyver Engineering Academy V12: member profiles, paid learning passes and
-- protected course content. Run after 001_learning_progress.sql, in the Supabase
-- SQL editor or with `supabase db push` (see docs/PAYMENTS_V12_ZH.md).
-- Idempotent: safe to run again. Stores no secrets, card data or bank accounts.
-- Browsers only ever use the publishable/anon key; every write to orders,
-- entitlements, payment_events and login_attempts is done by Edge Functions
-- with the service role, through the security-definer functions below.

create extension if not exists citext with schema extensions;

do $$
begin
  if exists (select 1 from information_schema.tables where table_schema = 'public' and table_name = 'profiles')
     and not exists (select 1 from information_schema.columns where table_schema = 'public' and table_name = 'profiles' and column_name = 'username') then
    raise exception 'public.profiles already exists with a different shape. Rename it (e.g. alter table public.profiles rename to profiles_old) and run this file again.';
  end if;
end $$;

-- ===================================================================== profiles
create table if not exists public.profiles (
  user_id uuid primary key references auth.users(id) on delete cascade,
  username extensions.citext not null,
  phone text not null,
  display_name text not null,
  email text,
  preferences jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint profiles_username_key unique (username),
  constraint profiles_phone_key unique (phone),
  constraint profiles_username_format check (username::text ~ '^[A-Za-z0-9_.-]{3,30}$'),
  constraint profiles_phone_format check (phone ~ '^\+[1-9][0-9]{7,14}$'),
  constraint profiles_display_name_length check (char_length(display_name) between 1 and 100),
  constraint profiles_email_length check (email is null or char_length(email) <= 320),
  constraint profiles_preferences_object check (jsonb_typeof(preferences) = 'object' and octet_length(preferences::text) <= 16384)
);

create or replace function public.academy_username_valid(p_username text)
returns boolean language sql immutable set search_path = '' as $$
  select p_username is not null
    and p_username ~ '^[A-Za-z0-9_.-]{3,30}$'
    and lower(p_username) <> all (array['admin', 'administrator', 'root', 'system', 'support', 'help', 'staff',
      'owner', 'official', 'security', 'billing', 'payment', 'payments', 'macgyver', 'academy', 'moderator', 'null', 'undefined']);
$$;

-- Profile row for every new auth user. Raising here aborts the auth.users insert,
-- so a sign-up with a missing/invalid/duplicate username or phone fails atomically
-- (GoTrue then answers "Database error saving new user"; the site should call
-- academy_check_available first to show a friendly message).
create or replace function public.academy_handle_new_user()
returns trigger language plpgsql security definer set search_path = '' as $$
declare
  meta jsonb := coalesce(new.raw_user_meta_data, '{}'::jsonb);
  v_username text := btrim(coalesce(meta ->> 'username', ''));
  v_phone text := btrim(coalesce(meta ->> 'phone', ''));
  v_name text := btrim(coalesce(meta ->> 'name', ''));
begin
  if not public.academy_username_valid(v_username) then
    raise exception 'academy_profile: username missing, invalid or reserved' using errcode = '22023';
  end if;
  if v_phone !~ '^\+[1-9][0-9]{7,14}$' then
    raise exception 'academy_profile: phone missing or not E.164' using errcode = '22023';
  end if;
  if v_name = '' then v_name := v_username; end if;
  if char_length(v_name) > 100 then
    raise exception 'academy_profile: name longer than 100 characters' using errcode = '22023';
  end if;
  begin
    insert into public.profiles (user_id, username, phone, display_name, email)
    values (new.id, v_username, v_phone, v_name, lower(new.email));
  exception when unique_violation then
    raise exception 'academy_profile: username or phone already registered' using errcode = '23505';
  end;
  return new;
end; $$;

create or replace function public.academy_sync_profile_email()
returns trigger language plpgsql security definer set search_path = '' as $$
begin
  update public.profiles set email = lower(new.email) where user_id = new.id;
  return new;
end; $$;

create or replace function public.academy_touch_updated_at()
returns trigger language plpgsql set search_path = '' as $$
begin
  new.updated_at := now();
  return new;
end; $$;

drop trigger if exists academy_on_auth_user_created on auth.users;
create trigger academy_on_auth_user_created after insert on auth.users
  for each row execute function public.academy_handle_new_user();
drop trigger if exists academy_on_auth_user_email_changed on auth.users;
create trigger academy_on_auth_user_email_changed after update of email on auth.users
  for each row when (old.email is distinct from new.email) execute function public.academy_sync_profile_email();
drop trigger if exists academy_profiles_touch on public.profiles;
create trigger academy_profiles_touch before update on public.profiles
  for each row execute function public.academy_touch_updated_at();

alter table public.profiles enable row level security;
revoke all on table public.profiles from public, anon, authenticated;
grant select on table public.profiles to authenticated;
grant update (display_name, preferences) on table public.profiles to authenticated;
grant all on table public.profiles to service_role;
drop policy if exists profiles_select_own on public.profiles;
create policy profiles_select_own on public.profiles for select to authenticated
  using ((select auth.uid()) = user_id);
drop policy if exists profiles_update_own on public.profiles;
create policy profiles_update_own on public.profiles for update to authenticated
  using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);

-- Sign-up form pre-check. Returns only two booleans (null when that argument is null);
-- an invalid or reserved value is reported as not available.
create or replace function public.academy_check_available(p_username text, p_phone text)
returns jsonb language sql stable security definer set search_path = '' as $$
  select jsonb_build_object(
    'usernameAvailable', case
      when p_username is null then null
      when not public.academy_username_valid(btrim(p_username)) then false
      else not exists (select 1 from public.profiles p
                       where p.username operator(extensions.=) btrim(p_username)::extensions.citext) end,
    'phoneAvailable', case
      when p_phone is null then null
      when btrim(p_phone) !~ '^\+[1-9][0-9]{7,14}$' then false
      else not exists (select 1 from public.profiles p where p.phone = btrim(p_phone)) end);
$$;

-- username → email for the username-login Edge Function (service role only).
create or replace function public.academy_login_email(p_username text)
returns text language sql stable security definer set search_path = '' as $$
  select p.email from public.profiles p
  where public.academy_username_valid(p_username)
    and p.username operator(extensions.=) p_username::extensions.citext;
$$;

-- ======================================================================== plans
create table if not exists public.plans (
  id text primary key check (id ~ '^[a-z0-9-]{1,40}$'),
  title text not null check (char_length(title) between 1 and 100),
  title_en text not null check (char_length(title_en) between 1 and 100),
  amount_twd integer not null check (amount_twd > 0),
  duration_days integer not null check (duration_days between 1 and 3660),
  active boolean not null default true,
  sort_order integer not null default 0,
  updated_at timestamptz not null default now()
);
-- Seed = public/academy/data/pricing.json (node tools/payments-v12/sync-pricing.mjs --sql prints this).
insert into public.plans (id, title, title_en, amount_twd, duration_days, sort_order) values
  ('all-30', '30 天學習通行證', '30-day learning pass', 299, 30, 1),
  ('all-365', '365 天學習通行證', '365-day learning pass', 2490, 365, 2)
on conflict (id) do update set title = excluded.title, title_en = excluded.title_en, amount_twd = excluded.amount_twd,
  duration_days = excluded.duration_days, sort_order = excluded.sort_order, active = true, updated_at = now();

alter table public.plans enable row level security;
revoke all on table public.plans from public, anon, authenticated;
grant select on table public.plans to anon, authenticated;
grant all on table public.plans to service_role;
drop policy if exists plans_read on public.plans;
create policy plans_read on public.plans for select to anon, authenticated using (true);

-- ===================================================================== fx_rates
create table if not exists public.fx_rates (
  currency text primary key check (currency ~ '^[A-Z]{3}$'),
  per_twd numeric not null check (per_twd > 0),
  source text not null default 'manual' check (char_length(source) <= 100),
  updated_at timestamptz not null default now()
);
insert into public.fx_rates (currency, per_twd, source) values ('TWD', 1, 'fixed') on conflict (currency) do nothing;

alter table public.fx_rates enable row level security;
revoke all on table public.fx_rates from public, anon, authenticated;
grant select on table public.fx_rates to anon, authenticated;
grant all on table public.fx_rates to service_role;
drop policy if exists fx_rates_read on public.fx_rates;
create policy fx_rates_read on public.fx_rates for select to anon, authenticated using (true);

-- ======================================================================= orders
create table if not exists public.orders (
  id text primary key check (id ~ '^MG[0-9A-F]{18}$'),
  user_id uuid references auth.users(id) on delete set null,
  plan_id text not null references public.plans(id),
  provider text not null check (provider in ('paypal', 'ecpay')),
  env text not null check (env in ('sandbox', 'live')),
  status text not null default 'pending'
    check (status in ('pending', 'paid', 'failed', 'review', 'refunded', 'reversed', 'revoked')),
  currency text not null check (currency ~ '^[A-Z]{3}$'),
  amount numeric(20, 2) not null check (amount > 0),
  amount_twd integer not null check (amount_twd > 0),
  fx_rate numeric not null check (fx_rate > 0),
  duration_days integer not null check (duration_days > 0),
  terms_version text not null check (char_length(terms_version) between 1 and 64),
  provider_order_id text check (provider_order_id is null or provider_order_id ~ '^[A-Za-z0-9-]{1,64}$'),
  provider_capture_id text check (provider_capture_id is null or provider_capture_id ~ '^[A-Za-z0-9-]{1,64}$'),
  last_error text check (last_error is null or char_length(last_error) <= 200),
  revoke_reason text check (revoke_reason is null or char_length(revoke_reason) <= 500),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  paid_at timestamptz,
  revoked_at timestamptz,
  constraint orders_ecpay_twd check (provider <> 'ecpay' or (currency = 'TWD' and amount = amount_twd))
);
create unique index if not exists orders_provider_order_uidx on public.orders (provider, provider_order_id) where provider_order_id is not null;
create unique index if not exists orders_provider_capture_uidx on public.orders (provider, provider_capture_id) where provider_capture_id is not null;
create index if not exists orders_user_created_idx on public.orders (user_id, created_at desc);
drop trigger if exists academy_orders_touch on public.orders;
create trigger academy_orders_touch before update on public.orders
  for each row execute function public.academy_touch_updated_at();

alter table public.orders enable row level security;
revoke all on table public.orders from public, anon, authenticated;
grant select on table public.orders to authenticated;
grant all on table public.orders to service_role;
drop policy if exists orders_select_own on public.orders;
create policy orders_select_own on public.orders for select to authenticated
  using ((select auth.uid()) = user_id);

-- ================================================================= entitlements
create table if not exists public.entitlements (
  order_id text primary key references public.orders(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  plan_id text not null references public.plans(id),
  env text not null check (env in ('sandbox', 'live')),
  starts_at timestamptz not null,
  expires_at timestamptz not null,
  revoked_at timestamptz,
  revoke_reason text check (revoke_reason is null or char_length(revoke_reason) <= 500),
  created_at timestamptz not null default now(),
  constraint entitlements_period check (expires_at > starts_at)
);
create index if not exists entitlements_user_active_idx on public.entitlements (user_id, expires_at desc) where revoked_at is null;

alter table public.entitlements enable row level security;
revoke all on table public.entitlements from public, anon, authenticated;
grant select on table public.entitlements to authenticated;
grant all on table public.entitlements to service_role;
drop policy if exists entitlements_select_own on public.entitlements;
create policy entitlements_select_own on public.entitlements for select to authenticated
  using ((select auth.uid()) = user_id);

-- =============================================== payment_events, login_attempts
create table if not exists public.payment_events (
  id bigint generated always as identity primary key,
  provider text not null check (provider in ('paypal', 'ecpay')),
  event_key text not null check (char_length(event_key) between 1 and 128),
  event_type text not null check (char_length(event_type) <= 100),
  order_id text references public.orders(id) on delete set null,
  result text not null check (char_length(result) <= 100),
  detail jsonb not null default '{}'::jsonb check (jsonb_typeof(detail) = 'object' and octet_length(detail::text) <= 8192),
  created_at timestamptz not null default now(),
  constraint payment_events_key unique (provider, event_key)
);
create index if not exists payment_events_order_idx on public.payment_events (order_id);

create table if not exists public.login_attempts (
  id bigint generated always as identity primary key,
  key_hash text not null check (key_hash ~ '^[0-9a-f]{64}$'),
  attempted_at timestamptz not null default now()
);
create index if not exists login_attempts_key_idx on public.login_attempts (key_hash, attempted_at);

alter table public.payment_events enable row level security;
alter table public.login_attempts enable row level security;
revoke all on table public.payment_events, public.login_attempts from public, anon, authenticated;
grant all on table public.payment_events, public.login_attempts to service_role;
-- No policies: browsers can neither read nor write these tables.

-- =============================================================== course_content
create table if not exists public.course_content (
  course_id text not null check (course_id ~ '^[A-Za-z0-9_-]{1,100}$'),
  stage_index integer not null check (stage_index between 0 and 999),
  revision text not null check (char_length(revision) between 1 and 128),
  payload jsonb not null check (octet_length(payload::text) <= 2000000),
  updated_at timestamptz not null default now(),
  primary key (course_id, stage_index)
);

-- ==================================================================== functions
-- True when p_user_id has a current, non-revoked pass. Answers only for the caller
-- itself (or service_role / direct database sessions), so it cannot be used to
-- probe other members.
create or replace function public.academy_has_access(p_user_id uuid)
returns boolean language sql stable security definer set search_path = '' as $$
  select p_user_id is not null
    and (p_user_id = (select auth.uid())
         or coalesce((select auth.role()), '') = 'service_role'
         or nullif(current_setting('request.jwt.claims', true), '') is null)
    and exists (select 1 from public.entitlements e
                where e.user_id = p_user_id and e.revoked_at is null
                  and e.starts_at <= now() and e.expires_at > now());
$$;

-- {active, expiresAt, planId}: expiresAt is the end of the caller's whole
-- (stacked) pass, null if never bought; planId is the plan in effect now (or last).
create or replace function public.academy_my_access()
returns jsonb language plpgsql stable security definer set search_path = '' as $$
declare
  uid uuid := auth.uid();
  v_plan text;
  v_last_plan text;
  v_expires timestamptz;
begin
  if uid is null then
    return jsonb_build_object('active', false, 'expiresAt', null, 'planId', null);
  end if;
  select e.plan_id into v_plan from public.entitlements e
   where e.user_id = uid and e.revoked_at is null and e.starts_at <= now() and e.expires_at > now()
   order by e.expires_at desc limit 1;
  select e.plan_id, e.expires_at into v_last_plan, v_expires from public.entitlements e
   where e.user_id = uid and e.revoked_at is null
   order by e.expires_at desc limit 1;
  return jsonb_build_object('active', v_plan is not null, 'expiresAt', v_expires, 'planId', coalesce(v_plan, v_last_plan));
end; $$;

-- Marks a verified order paid and grants (once) a pass that starts at
-- max(now, current expiry). Idempotent; refuses refunded/reversed/revoked orders.
create or replace function public.academy_grant_entitlement(p_order_id text)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare
  o public.orders;
  e public.entitlements;
  v_now timestamptz := now();
  v_start timestamptz;
  v_until timestamptz;
begin
  select * into o from public.orders where id = p_order_id for update;
  if not found then
    raise exception 'academy: order % not found', p_order_id using errcode = 'P0002';
  end if;
  if o.status in ('refunded', 'reversed', 'revoked') then
    return jsonb_build_object('granted', false, 'status', o.status, 'orderId', o.id);
  end if;
  if o.user_id is null then
    raise exception 'academy: order % has no member', o.id using errcode = '22023';
  end if;
  perform pg_advisory_xact_lock(hashtextextended('academy-entitlement:' || o.user_id::text, 0));
  select * into e from public.entitlements where order_id = o.id;
  if not found then
    select greatest(v_now, coalesce(max(x.expires_at), v_now)) into v_start
      from public.entitlements x where x.user_id = o.user_id and x.revoked_at is null;
    insert into public.entitlements (order_id, user_id, plan_id, env, starts_at, expires_at)
    values (o.id, o.user_id, o.plan_id, o.env, v_start, v_start + make_interval(days => o.duration_days))
    returning * into e;
  end if;
  update public.orders set status = 'paid', paid_at = coalesce(paid_at, v_now), last_error = null
   where id = o.id and status <> 'paid';
  select max(x.expires_at) into v_until from public.entitlements x
   where x.user_id = o.user_id and x.revoked_at is null;
  return jsonb_build_object('granted', e.revoked_at is null, 'status', 'paid', 'orderId', o.id,
    'startsAt', e.starts_at, 'expiresAt', e.expires_at, 'accessExpiresAt', v_until);
end; $$;

-- Revokes the pass bought by an order (refund, reversal/chargeback or manual).
-- p_reason starting with "refund" → status refunded; "revers"/"chargeback" →
-- reversed; anything else → revoked. Later stacked passes move earlier so the
-- member keeps exactly the time still paid for. Idempotent. Does NOT move money:
-- refunds themselves are made in the PayPal / ECPay dashboards.
create or replace function public.academy_revoke_entitlement(p_order_id text, p_reason text)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare
  o public.orders;
  v_reason text := left(btrim(coalesce(p_reason, '')), 500);
  v_status text;
  v_now timestamptz := now();
  v_cursor timestamptz;
  v_revoked integer;
  r record;
begin
  if char_length(v_reason) < 3 then
    raise exception 'academy: a revoke reason is required' using errcode = '22023';
  end if;
  select * into o from public.orders where id = p_order_id for update;
  if not found then
    raise exception 'academy: order % not found', p_order_id using errcode = 'P0002';
  end if;
  v_status := case when o.status in ('refunded', 'reversed', 'revoked') then o.status
                   when v_reason ~* '^refund' then 'refunded'
                   when v_reason ~* '^(revers|chargeback)' then 'reversed'
                   else 'revoked' end;
  update public.orders set status = v_status, revoked_at = coalesce(revoked_at, v_now),
         revoke_reason = coalesce(revoke_reason, v_reason)
   where id = o.id;
  if o.user_id is not null then
    perform pg_advisory_xact_lock(hashtextextended('academy-entitlement:' || o.user_id::text, 0));
    update public.entitlements set revoked_at = v_now, revoke_reason = v_reason
     where order_id = o.id and revoked_at is null;
    get diagnostics v_revoked = row_count;
    if v_revoked > 0 then
      select greatest(v_now, coalesce(max(x.expires_at), v_now)) into v_cursor
        from public.entitlements x
       where x.user_id = o.user_id and x.revoked_at is null and x.starts_at <= v_now;
      for r in select x.order_id, x.starts_at, x.expires_at from public.entitlements x
                where x.user_id = o.user_id and x.revoked_at is null and x.starts_at > v_now
                order by x.starts_at, x.order_id loop
        if r.starts_at > v_cursor then
          update public.entitlements set starts_at = v_cursor, expires_at = v_cursor + (r.expires_at - r.starts_at)
           where order_id = r.order_id;
          v_cursor := v_cursor + (r.expires_at - r.starts_at);
        else
          v_cursor := greatest(v_cursor, r.expires_at);
        end if;
      end loop;
    end if;
  end if;
  return jsonb_build_object('revoked', true, 'orderId', o.id, 'status', v_status);
end; $$;

-- Sliding-window counter for username-login (service role only). Keys are HMACs.
create or replace function public.academy_login_attempt(p_key_hash text, p_limit integer, p_window_seconds integer)
returns jsonb language plpgsql security definer set search_path = '' as $$
declare
  v_now timestamptz := now();
  v_window interval := make_interval(secs => greatest(1, least(p_window_seconds, 86400)));
  v_count integer;
  v_oldest timestamptz;
begin
  if p_key_hash !~ '^[0-9a-f]{64}$' or p_limit < 1 then
    raise exception 'academy: invalid rate-limit arguments' using errcode = '22023';
  end if;
  perform pg_advisory_xact_lock(hashtextextended('academy-login:' || p_key_hash, 0));
  delete from public.login_attempts where key_hash = p_key_hash and attempted_at <= v_now - v_window;
  select count(*), min(attempted_at) into v_count, v_oldest from public.login_attempts where key_hash = p_key_hash;
  if v_count >= p_limit then
    return jsonb_build_object('allowed', false,
      'retryAfter', greatest(1, ceil(extract(epoch from (v_oldest + v_window - v_now)))::integer));
  end if;
  insert into public.login_attempts (key_hash, attempted_at) values (p_key_hash, v_now);
  if random() < 0.02 then
    delete from public.login_attempts where attempted_at < v_now - interval '2 days';
  end if;
  return jsonb_build_object('allowed', true, 'retryAfter', 0);
end; $$;

-- Free policy: stage_index 0 of every course is public; other stages need a pass.
alter table public.course_content enable row level security;
revoke all on table public.course_content from public, anon, authenticated;
grant select on table public.course_content to anon, authenticated;
grant all on table public.course_content to service_role;
drop policy if exists course_content_read on public.course_content;
create policy course_content_read on public.course_content for select to anon, authenticated
  using (stage_index = 0 or (select public.academy_has_access((select auth.uid()))));

-- ============================================================ function grants
revoke all on function public.academy_username_valid(text) from public, anon, authenticated;
revoke all on function public.academy_handle_new_user() from public, anon, authenticated;
revoke all on function public.academy_sync_profile_email() from public, anon, authenticated;
revoke all on function public.academy_touch_updated_at() from public, anon, authenticated;
revoke all on function public.academy_check_available(text, text) from public;
grant execute on function public.academy_check_available(text, text) to anon, authenticated, service_role;
revoke all on function public.academy_login_email(text) from public, anon, authenticated;
grant execute on function public.academy_login_email(text) to service_role;
revoke all on function public.academy_has_access(uuid) from public;
-- anon needs EXECUTE because the course_content policy calls it; it answers false for anyone but the caller.
grant execute on function public.academy_has_access(uuid) to anon, authenticated, service_role;
revoke all on function public.academy_my_access() from public;
grant execute on function public.academy_my_access() to anon, authenticated, service_role;
revoke all on function public.academy_grant_entitlement(text) from public, anon, authenticated;
grant execute on function public.academy_grant_entitlement(text) to service_role;
revoke all on function public.academy_revoke_entitlement(text, text) from public, anon, authenticated;
grant execute on function public.academy_revoke_entitlement(text, text) to service_role;
revoke all on function public.academy_login_attempt(text, integer, integer) from public, anon, authenticated;
grant execute on function public.academy_login_attempt(text, integer, integer) to service_role;

-- ======================================= optional: fx-refresh job every 12 hours (V13)
-- Enable the pg_cron and pg_net extensions (Dashboard → Database → Extensions),
-- store the same value as the CRON_SECRET function secret in Vault, then run:
--
-- select vault.create_secret('<same value as CRON_SECRET>', 'academy_cron_secret');
-- select cron.schedule('academy-fx-refresh', '17 */12 * * *', $job$
--   select net.http_post(
--     url := 'https://<project-ref>.supabase.co/functions/v1/fx-refresh',
--     headers := jsonb_build_object(
--       'Content-Type', 'application/json',
--       'x-cron-secret', (select decrypted_secret from vault.decrypted_secrets where name = 'academy_cron_secret')),
--     body := '{}'::jsonb,
--     timeout_milliseconds := 15000);
-- $job$);
--
-- Check: select * from cron.job_run_details order by start_time desc limit 5;
--        select currency, per_twd, updated_at from public.fx_rates order by currency;
-- Remove: select cron.unschedule('academy-fx-refresh');
