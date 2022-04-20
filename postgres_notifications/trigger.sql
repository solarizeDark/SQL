create or replace function deletion_attempt_trigger()
	returns trigger as
$$
declare 
	channel text := TG_ARGV[0];
begin
	perform (
		with message as (
			select concat(TG_ARGV[1], ' ',
					(select current_user)::text) as mes
		)
		select pg_notify(channel, mes)
			from message
	);
	return null;
end
$$ language plpgsql;

create trigger deletion_attempt_trigger
    before delete on public.important
    for each row
execute procedure del_con('important_channel', 'Deletion attempt user: ');