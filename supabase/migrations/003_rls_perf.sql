-- planti-dex · políticas RLS más eficientes
-- (select is_household()) se evalúa una vez por consulta en lugar de una vez por fila.
-- Mismas reglas que 001: solo la casa lee y escribe; cada quien borra solo lo suyo.

drop policy if exists "household read members" on household_members;
create policy "household read members" on household_members for select to authenticated using ((select is_household()));

drop policy if exists "household read plants"  on plants;
drop policy if exists "household write plants" on plants;
create policy "household read plants"  on plants for select to authenticated using ((select is_household()));
create policy "household write plants" on plants for all    to authenticated using ((select is_household())) with check ((select is_household()));

drop policy if exists "household read log"  on care_log;
drop policy if exists "household write log" on care_log;
drop policy if exists "own delete log"      on care_log;
create policy "household read log"  on care_log for select to authenticated using ((select is_household()));
create policy "household write log" on care_log for insert to authenticated with check ((select is_household()) and done_by = (select auth.uid()));
create policy "own delete log"      on care_log for delete to authenticated using ((select is_household()) and done_by = (select auth.uid()));
