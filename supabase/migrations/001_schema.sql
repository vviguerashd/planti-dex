-- planti-dex · esquema base
-- Correr una sola vez en Supabase → SQL Editor. Idempotente donde se puede.

create extension if not exists pgcrypto;

-- Quién vive en la casa (Vic y Fer). Solo estas cuentas leen y escriben.
create table if not exists household_members (
  user_id      uuid primary key references auth.users(id) on delete cascade,
  display_name text not null
);

-- Fuente única de verdad de "¿esta sesión es de la casa?"
create or replace function public.is_household()
returns boolean
language sql stable security definer set search_path = public
as $$
  select exists (select 1 from household_members where user_id = auth.uid());
$$;

-- Una fila por planta. El id ('P07') es lo que se escribe en el sticker NFC y nunca cambia.
create table if not exists plants (
  id                  text primary key check (id ~ '^P[0-9]{2,3}$'),
  nickname            text,
  name                text not null,
  species             text,
  zone                text not null check (zone in ('escaleras','estudio','sala','jardin','bufetera')),
  tracking            text not null check (tracking in ('mascota','esqueje','zona','temporal')),
  location_note       text,
  indoor              boolean not null default false,
  medium              text,
  light               text,
  water_interval_days int  not null check (water_interval_days > 0),
  care_action         text not null default 'watered' check (care_action in ('watered','water_changed')),
  toxic_pets          text check (toxic_pets in ('si','irritante')),
  parent_id           text references plants(id),   -- linaje: de qué planta salió un esqueje
  notes               text,
  active              boolean not null default true,
  created_at          timestamptz not null default now()
);

-- Cada cuidado registrado. done_by se llena solo con la sesión.
create table if not exists care_log (
  id         uuid primary key default gen_random_uuid(),
  plant_id   text not null references plants(id) on delete cascade,
  done_at    timestamptz not null default now(),
  done_by    uuid references auth.users(id) default auth.uid(),
  action     text not null check (action in ('watered','checked_ok','water_changed','transplanted','pruned','fertilized','photo')),
  condition  text check (condition in ('bien','regular','mal')),
  note       text
);
create index if not exists care_log_plant_time on care_log (plant_id, done_at desc);

-- RLS: nada público. Solo miembros de la casa.
alter table household_members enable row level security;
alter table plants            enable row level security;
alter table care_log          enable row level security;

revoke all on household_members, plants, care_log from anon;

drop policy if exists "household read members" on household_members;
create policy "household read members" on household_members for select to authenticated using (is_household());

drop policy if exists "household read plants"   on plants;
drop policy if exists "household write plants"  on plants;
create policy "household read plants"  on plants for select to authenticated using (is_household());
create policy "household write plants" on plants for all    to authenticated using (is_household()) with check (is_household());

drop policy if exists "household read log"   on care_log;
drop policy if exists "household write log"  on care_log;
create policy "household read log"  on care_log for select to authenticated using (is_household());
create policy "household write log" on care_log for insert to authenticated with check (is_household() and done_by = auth.uid());
-- Borrar un registro equivocado: solo quien lo hizo.
drop policy if exists "own delete log" on care_log;
create policy "own delete log" on care_log for delete to authenticated using (is_household() and done_by = auth.uid());
