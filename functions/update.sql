create or replace function update_auto_price()
returns trigger as $auto_price_update$
begin
	update Orders
	set order_price = order_price - OLD.price + NEW.price
	where NEW.automobile_id = automobile_id;
	return NEW;
end;
$auto_price_update$ language plpgsql volatile;


create or replace function update_auto_options()
returns trigger as $auto_options_update$
begin
	update Orders
	set order_price = order_price - OLD.options_ + NEW.options_
	where NEW.autosalon_id = autosalon_id;
	return NEW;
end;
$auto_options_update$ language plpgsql volatile;


create trigger auto_price_update
after insert or update or delete on Automobiles
for each row execute procedure update_auto_price();


create trigger auto_options_update
after insert or update or delete on Autosalons
for each row execute procedure update_auto_options();