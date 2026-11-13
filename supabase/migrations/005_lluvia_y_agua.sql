-- planti-dex · lluvia y plantas en agua
-- 1) Las plantas en agua (esquejes) se rellenan una vez al mes.
update plants set water_interval_days = 30 where care_action = 'water_changed';

-- 2) Nueva acción "rained": se mojó con la lluvia (o la sacaron a la lluvia).
--    Reinicia el conteo de riego de las plantas de tierra, sin decir que alguien regó.
alter table care_log drop constraint if exists care_log_action_check;
alter table care_log add constraint care_log_action_check
  check (action in ('watered','checked_ok','water_changed','transplanted','pruned','fertilized','photo','rained'));
