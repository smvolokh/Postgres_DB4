create or replace procedure clear_table(name_table text)
language plpgsql as $$
begin
	if name_table = 'Automobiles' then
		truncate Automobiles cascade;
	end if;
	if name_table = 'Autosalons' then
		truncate Autosalons cascade;
	end if;
	if name_table = 'Orders' then
		truncate Orders cascade;
	end if;
end$$;