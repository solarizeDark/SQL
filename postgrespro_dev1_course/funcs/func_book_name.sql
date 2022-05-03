create function book_name(bid integer)
returns text
as $$

	select b.title || ' ' ||
	string_agg(author_name(a.last_name, a.first_name, a.middle_name), 
	', ' order by aus.seq_num) 
	from books b 
	join authorship aus on aus.book_id = b.book_id
	join authors a on a.author_id = aus.author_id 
	where b.book_id = bid
	group by b.title; 

$$ volatile language sql
