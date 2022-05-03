create function author_name (last_name text, first_name text, 
				middle_name text default null) 
returns text
as $$
	select last_name || ' ' || substring(first_name, 1, 1) || '.' || 
			coalesce(substring(middle_name, 1, 1) || '.', '');
$$ volatile language sql
