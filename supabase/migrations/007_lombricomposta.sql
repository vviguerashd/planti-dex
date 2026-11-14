-- planti-dex · lombricomposta del patio trasero (dos depósitos). RLS desde el inicio.
create table if not exists compost_bins (
  id     text primary key check (id ~ '^L[0-9]$'),
  name   text not null,
  notes  text,
  active boolean not null default true
);
create table if not exists compost_log (
  id       uuid primary key default gen_random_uuid(),
  bin_id   text not null references compost_bins(id) on delete cascade,
  done_at  timestamptz not null default now(),
  done_by  uuid references auth.users(id) default auth.uid(),
  action   text not null check (action in ('feed','bedding','moisture_ok','moisture_dry','moisture_wet','drained','harvest')),
  note     text
);
create index if not exists compost_log_bin_time on compost_log (bin_id, done_at desc);

alter table compost_bins enable row level security;
alter table compost_log  enable row level security;
revoke all on compost_bins, compost_log from anon;

drop policy if exists "household read bins"  on compost_bins;
drop policy if exists "household write bins" on compost_bins;
create policy "household read bins"  on compost_bins for select to authenticated using ((select is_household()));
create policy "household write bins" on compost_bins for all    to authenticated using ((select is_household())) with check ((select is_household()));

drop policy if exists "household read compost"  on compost_log;
drop policy if exists "household write compost" on compost_log;
drop policy if exists "own delete compost"      on compost_log;
create policy "household read compost"  on compost_log for select to authenticated using ((select is_household()));
create policy "household write compost" on compost_log for insert to authenticated with check ((select is_household()) and done_by = (select auth.uid()));
create policy "own delete compost"      on compost_log for delete to authenticated using ((select is_household()) and done_by = (select auth.uid()));

insert into compost_bins (id, name, notes) values
  ('L1', 'Depósito 1 · cubetas', 'Dos cubetas de 19 L apiladas: arriba tierra y lombrices (fondo perforado), abajo junta el líquido.'),
  ('L2', 'Depósito 2 · talavera', 'Maceta de talavera con girasoles sobre base de fierro, con hoyos abajo.')
on conflict (id) do nothing;
