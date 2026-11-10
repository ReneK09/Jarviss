-- Arenly push notifications (run once in Supabase → SQL Editor, after schema.sql)

-- 1) Devices that want notifications. Each signed-in user only sees / changes their own rows.
create table if not exists public.push_subscriptions (
  endpoint    text primary key,
  user_id     uuid not null default auth.uid() references auth.users (id) on delete cascade,
  p256dh      text not null,
  auth        text not null,
  club_id     text,
  club_slug   text,
  nation_id   text,
  prefs       jsonb not null default '{"goals": true, "matchday": true, "lineup": true}'::jsonb,
  app_url     text,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);
alter table public.push_subscriptions enable row level security;
drop policy if exists "push: read own"   on public.push_subscriptions;
drop policy if exists "push: insert own" on public.push_subscriptions;
drop policy if exists "push: update own" on public.push_subscriptions;
drop policy if exists "push: delete own" on public.push_subscriptions;
create policy "push: read own"   on public.push_subscriptions for select using (auth.uid() = user_id);
create policy "push: insert own" on public.push_subscriptions for insert with check (auth.uid() = user_id);
create policy "push: update own" on public.push_subscriptions for update using (auth.uid() = user_id) with check (auth.uid() = user_id);
create policy "push: delete own" on public.push_subscriptions for delete using (auth.uid() = user_id);

-- 2) What was already sent per match (only the Edge Function uses it – no policies on purpose).
create table if not exists public.push_state (
  event_id    text primary key,
  slug        text,
  state       text,
  home_score  int,
  away_score  int,
  kickoff     timestamptz,
  sent        jsonb not null default '{}'::jsonb,
  updated_at  timestamptz not null default now()
);
alter table public.push_state enable row level security;

-- 3) Call the Edge Function every minute.
--    Replace <CRON_SECRET> with the same value you stored as the CRON_SECRET secret of the function.
create extension if not exists pg_cron;
create extension if not exists pg_net;
select cron.unschedule(jobid) from cron.job where jobname = 'arenly-push-watch';
select cron.schedule(
  'arenly-push-watch',
  '* * * * *',
  $$
  select net.http_post(
    url     := 'https://hyomumbaokxfqhhvrgpf.supabase.co/functions/v1/push-watch',
    headers := jsonb_build_object('Content-Type', 'application/json', 'x-cron-secret', '<CRON_SECRET>'),
    body    := '{}'::jsonb,
    timeout_milliseconds := 25000
  );
  $$
);
