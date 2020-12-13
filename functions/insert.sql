create or replace procedure insert_Automobiles(temp_automobile_id char(5),
											   temp_model text,
											   temp_price integer)
language plpgsql as $$											   
begin
	insert into Automobiles(automobile_id, model, price)
		values (temp_automobile_id, temp_model, temp_price)
			on conflict("automobile_id") do update set
			model = excluded.model,
			price = excluded.price;
end$$;

create or replace procedure insert_Autosalons(temp_autosalon_id char(5),
											  temp_autosalon_adress text,
										      temp_model text,
											  temp_in_stock boolean,
											  temp_options_ integer)
language plpgsql as $$												  
begin
	insert into Autosalons(autosalon_id, autosalon_adress, model, in_stock, options_)
		values (temp_autosalon_id, temp_autosalon_adress, temp_model, temp_in_stock, temp_options_)
			on conflict("autosalon_id") do update set
			autosalon_adress = excluded.autosalon_adress,
			model = excluded.model,
			in_stock = excluded.in_stock,
			options_ = excluded.options_;
end$$;

create or replace procedure insert_Orders(temp_order_id char(5), temp_automobile_id char(5), temp_autosalon_id char(5), temp_customer text, temp_model text)
language plpgsql as $$
declare
    auto_price integer;
    options_price integer;
    full_price integer;
begin
    auto_price = (select price from Automobiles where automobile_id = temp_automobile_id);
    options_price  = (select options_ from Autosalons where autosalon_id = temp_autosalon_id);
    full_price = auto_price + options_price;

	insert into Orders(order_id, automobile_id, autosalon_id, customer, model, order_price)
		values (temp_order_id, temp_automobile_id, temp_autosalon_id, temp_customer, temp_model, full_price)
			on conflict("order_id") do update set
			automobile_id = excluded.automobile_id,
			autosalon_id = excluded.autosalon_id,
			customer = excluded.customer,
			model = excluded.model,
			order_price = excluded.order_price;
end$$;