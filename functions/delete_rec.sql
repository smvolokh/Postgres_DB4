create or replace procedure delete_rec(table_name text, id_rec char(5))
language plpgsql as $$
begin
	if table_name = 'Automobiles' then
		delete from Automobiles
		where automobile_id = id_rec;
	end if;
	if table_name = 'Autosalons' then
		delete from Autosalons
		where autosalon_id = id_rec;
	end if;
	if table_name = 'Orders' then
		delete from Orders
		where order_id = id_rec;
	end if;
end$$;
	