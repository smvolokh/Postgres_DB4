create or replace function output_Automobiles()
returns table (automobile_id char(5),
			   model text,
			   price integer)
			   as $$
begin
	return query (select * from Automobiles);
end;
$$ language plpgsql volatile;	


create or replace function output_Autosalons()
returns table (autosalon_id char(5),
			   autosalon_adress text,
			   model text,
			   in_stock boolean,
			   options_ integer)
			   as $$
begin
	return query (select * from Autosalons);
end;
$$ language plpgsql volatile;


create or replace function output_Orders()
returns table(order_id char(5),
			  automobile_id char(5),
			  autosalon_id char(5),
			  customer text,
			  model text,
			  order_price integer)
			  as $$
begin
	return query (select * from Orders);
end;
$$ language plpgsql volatile;