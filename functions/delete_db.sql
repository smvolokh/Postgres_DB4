create or replace procedure delete_db(db_name text, pass_ text)
language plpgsql as $$
begin
	perform pg_terminate_backend(pg_stat_activity.pid)
	from pg_stat_activity
	where pg_stat_activity.datname = db_name and pid != pg_backend_pid();
	perform dblink_exec('dbname='||current_database()||' user='||current_user||
	' password='|| pass_, 'drop database if exists '|| db_name);
end$$;
