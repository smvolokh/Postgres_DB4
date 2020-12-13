create or replace procedure delete_model(model_temp text)
language plpgsql as $$
begin
	delete from Orders o
	where o.model = model_temp;
end$$;