-- Arenly Tippspiel (run once in Supabase → SQL Editor, after schema.sql)

-- Tipprunden, Mitglieder, Tipps
create table if not exists public.tip_groups (
  id          uuid primary key default gen_random_uuid(),
  name        text not null check (char_length(name) between 2 and 40),
  code        text not null unique,
  league      text not null default 'ger.1',
  owner       uuid not null default auth.uid() references auth.users (id) on delete cascade,
  created_at  timestamptz not null default now()
);
create table if not exists public.tip_members (
  group_id      uuid not null references public.tip_groups (id) on delete cascade,
  user_id       uuid not null default auth.uid() references auth.users (id) on delete cascade,
  display_name  text,
  joined_at     timestamptz not null default now(),
  primary key (group_id, user_id)
);
create table if not exists public.tips (
  user_id     uuid not null default auth.uid() references auth.users (id) on delete cascade,
  event_id    text not null,
  slug        text not null,
  kickoff     timestamptz not null,
  home        int  not null check (home between 0 and 30),
  away        int  not null check (away between 0 and 30),
  updated_at  timestamptz not null default now(),
  primary key (user_id, event_id)
);

-- the database (not the phone) stamps every save – the app only counts tips saved before the real kick-off
create or replace function public.tips_stamp() returns trigger language plpgsql as $$
begin new.updated_at := now(); return new; end $$;
drop trigger if exists tips_stamp on public.tips;
create trigger tips_stamp before insert or update on public.tips for each row execute function public.tips_stamp();

-- helpers (security definer avoids recursive row-level-security checks)
create or replace function public.is_tip_member(g uuid) returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (select 1 from public.tip_members where group_id = g and user_id = auth.uid());
$$;
create or replace function public.shares_tip_group(other uuid) returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (select 1 from public.tip_members a join public.tip_members b on a.group_id = b.group_id
                 where a.user_id = auth.uid() and b.user_id = other);
$$;

-- row level security
alter table public.tip_groups  enable row level security;
alter table public.tip_members enable row level security;
alter table public.tips        enable row level security;

drop policy if exists "tip_groups: members read" on public.tip_groups;
create policy "tip_groups: members read" on public.tip_groups for select using (public.is_tip_member(id));

drop policy if exists "tip_members: members read"  on public.tip_members;
drop policy if exists "tip_members: leave"         on public.tip_members;
drop policy if exists "tip_members: rename self"   on public.tip_members;
create policy "tip_members: members read" on public.tip_members for select using (public.is_tip_member(group_id));
create policy "tip_members: leave"        on public.tip_members for delete using (user_id = auth.uid());
create policy "tip_members: rename self"  on public.tip_members for update using (user_id = auth.uid()) with check (user_id = auth.uid());

drop policy if exists "tips: read own or after kick-off" on public.tips;
drop policy if exists "tips: insert own before kick-off" on public.tips;
drop policy if exists "tips: update own before kick-off" on public.tips;
create policy "tips: read own or after kick-off" on public.tips for select
  using (user_id = auth.uid() or (kickoff < now() and public.shares_tip_group(user_id)));
create policy "tips: insert own before kick-off" on public.tips for insert with check (user_id = auth.uid() and kickoff > now());
create policy "tips: update own before kick-off" on public.tips for update
  using (user_id = auth.uid() and kickoff > now()) with check (user_id = auth.uid() and kickoff > now());

-- create / join a Tipprunde
create or replace function public.create_tip_group(p_name text, p_display text, p_league text default 'ger.1')
returns public.tip_groups language plpgsql security definer set search_path = '' as $$
declare g public.tip_groups; c text;
begin
  if auth.uid() is null then raise exception 'Bitte melde dich an.'; end if;
  loop
    c := upper(substr(md5(random()::text || clock_timestamp()::text), 1, 6));
    exit when not exists (select 1 from public.tip_groups where code = c);
  end loop;
  insert into public.tip_groups (name, code, league, owner) values (trim(p_name), c, coalesce(p_league, 'ger.1'), auth.uid()) returning * into g;
  insert into public.tip_members (group_id, user_id, display_name) values (g.id, auth.uid(), p_display);
  return g;
end $$;

create or replace function public.join_tip_group(p_code text, p_display text)
returns public.tip_groups language plpgsql security definer set search_path = '' as $$
declare g public.tip_groups;
begin
  if auth.uid() is null then raise exception 'Bitte melde dich an.'; end if;
  select * into g from public.tip_groups where code = upper(trim(p_code));
  if not found then raise exception 'Diesen Code gibt es nicht.'; end if;
  insert into public.tip_members (group_id, user_id, display_name) values (g.id, auth.uid(), p_display)
    on conflict (group_id, user_id) do nothing;
  return g;
end $$;

revoke all on function public.create_tip_group(text, text, text) from public, anon;
revoke all on function public.join_tip_group(text, text) from public, anon;
grant execute on function public.create_tip_group(text, text, text) to authenticated;
grant execute on function public.join_tip_group(text, text) to authenticated;
