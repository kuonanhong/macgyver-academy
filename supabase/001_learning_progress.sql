-- Run in the owner's Supabase SQL editor. No service-role key belongs in HTML.
create table if not exists public.academy_progress (
 user_id uuid not null references auth.users(id) on delete cascade,
 project_id text not null check(project_id ~ '^[a-zA-Z0-9_-]{1,100}$'),
 payload jsonb not null,
 revision bigint not null check(revision > 0 and revision < 9007199254740991),
 primary key(user_id,project_id),
 constraint valid_learning_payload check(
  jsonb_typeof(payload)='object' and payload ?& array['completed','assembly','notes'] and
  jsonb_typeof(payload->'completed')='array' and jsonb_array_length(payload->'completed')<=5000 and
  jsonb_typeof(payload->'assembly')='array' and jsonb_array_length(payload->'assembly')<=5000 and
  jsonb_typeof(payload->'notes')='string' and length(payload->>'notes')<=20000 and
  octet_length(payload::text)<=180000)
);
alter table public.academy_progress enable row level security;
revoke all on public.academy_progress from public,anon,authenticated;
grant select,insert,update,delete on public.academy_progress to authenticated;
drop policy if exists learner_read on public.academy_progress;
create policy learner_read on public.academy_progress for select to authenticated using((select auth.uid())=user_id);
drop policy if exists learner_insert on public.academy_progress;
create policy learner_insert on public.academy_progress for insert to authenticated with check((select auth.uid())=user_id);
drop policy if exists learner_update on public.academy_progress;
create policy learner_update on public.academy_progress for update to authenticated using((select auth.uid())=user_id) with check((select auth.uid())=user_id);
drop policy if exists learner_delete on public.academy_progress;
create policy learner_delete on public.academy_progress for delete to authenticated using((select auth.uid())=user_id);
create or replace function public.academy_save_progress(p_project_id text,p_payload jsonb,p_expected_revision bigint default null)
returns setof public.academy_progress language plpgsql security invoker set search_path='' as $$
declare saved public.academy_progress; uid uuid := auth.uid(); tick bigint := floor(extract(epoch from clock_timestamp())*1000)::bigint;
begin
 if uid is null then raise exception 'Authentication required' using errcode='28000'; end if;
 if p_expected_revision is null then
  insert into public.academy_progress(user_id,project_id,payload,revision)
  values(uid,p_project_id,p_payload,tick) on conflict do nothing returning * into saved;
 else
  update public.academy_progress set payload=p_payload,revision=greatest(tick,revision+1)
  where user_id=uid and project_id=p_project_id and revision=p_expected_revision returning * into saved;
 end if;
 if saved.user_id is null then raise exception 'Learning progress changed on another device' using errcode='MG409'; end if;
 return next saved;
end; $$;
revoke all on function public.academy_save_progress(text,jsonb,bigint) from public,anon;
grant execute on function public.academy_save_progress(text,jsonb,bigint) to authenticated;
