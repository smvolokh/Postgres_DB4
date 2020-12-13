create or replace procedure install_dblink()
language plpgsql
as $$
begin
	create extension if not exists dblink;
end
$$;

-- create proc for dblink ($2, $1 - args of proc)
create or replace procedure create_db(text, text)
language plpgsql
as $$
begin
	perform dblink_exec('dbname='||current_database()||' user='||current_user||' password='|| $2,
        'create database ' || $1 || ' with owner= '|| current_user);
end
$$;

create or replace function output_db()
returns table (id name) as $$
begin
	return query (select datname from pg_database);
end;
$$ language plpgsql volatile;