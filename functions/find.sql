create or replace function find(model_to_find text)
returns table (autosalon_id char(5), autosalon_adress text,
			   model text, in_stock boolean, options_ integer)
			   as $$
begin
	return query (select * from Autosalons aus
				  where aus.model = model_to_find);
end;
$$ language plpgsql volatile;