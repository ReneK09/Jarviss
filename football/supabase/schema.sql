-- Arenly: user profiles (run once in Supabase → SQL Editor)
-- Each signed-in user can read and write only their own row.

create table if not exists public.profiles (
  id          uuid primary key references auth.users (id) on delete cascade,
  name        text,
  club        jsonb,      -- { id, slug, name, logo }
  nation      jsonb,      -- { id, slug, name, logo }
  theme       jsonb,      -- { p: '#rrggbb', s: '#rrggbb' }  (club colours)
  favs        jsonb not null default '[]'::jsonb,
  created_at  timestamptz not null default now(),
  updated_at  timestamptz not null default now()
);

alter table public.profiles enable row level security;

drop policy if exists "profiles: read own"   on public.profiles;
drop policy if exists "profiles: insert own" on public.profiles;
drop policy if exists "profiles: update own" on public.profiles;
drop policy if exists "profiles: delete own" on public.profiles;

create policy "profiles: read own"   on public.profiles for select using (auth.uid() = id);
create policy "profiles: insert own" on public.profiles for insert with check (auth.uid() = id);
create policy "profiles: update own" on public.profiles for update using (auth.uid() = id) with check (auth.uid() = id);
create policy "profiles: delete own" on public.profiles for delete using (auth.uid() = id);

-- Create the profile row automatically when someone signs up (name from the sign-up form).
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer set search_path = ''
as $$
begin
  insert into public.profiles (id, name)
  values (new.id, coalesce(new.raw_user_meta_data ->> 'name', new.raw_user_meta_data ->> 'full_name'))
  on conflict (id) do nothing;
  return new;
end;
$$;

drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();
