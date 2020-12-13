create or replace procedure clear_all()
language plpgsql as $$
begin
	truncate Automobiles cascade;
	truncate Autosalons cascade;
	truncate Orders cascade;
end$$;