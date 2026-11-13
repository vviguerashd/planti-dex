-- planti-dex · plantas que hay que tapar o meter cuando hay helada.
alter table plants add column if not exists frost_sensitive boolean not null default false;
update plants set frost_sensitive = true where id in ('P04', 'P18', 'P24');   -- las tres bugambilias
