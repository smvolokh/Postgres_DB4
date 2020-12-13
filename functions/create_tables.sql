
create or replace procedure create_tables()
language plpgsql as $$
begin
	create table Automobiles (
	automobile_id char(5) unique not null,
	model text unique not null,
	price integer not null,
	check(price > 0),
	primary key (automobile_id)
	);

	create table Autosalons (
	autosalon_id char(5) unique not null,
	autosalon_adress text not null,
	model text not null,
	in_stock boolean not null,
	options_ integer not null,
	check(options_ >= 0),
	primary key (autosalon_id)
	);

	create table Orders (
	order_id char(5) unique not null,
	automobile_id char(5) not null,
	autosalon_id char(5) not null,
	customer text not null,
	model text not null,
	order_price integer not null,
	primary key (order_id),
	foreign key (model) references Automobiles(model) on delete cascade
	);
	
	create index model_index on Autosalons(model);
end;
$$