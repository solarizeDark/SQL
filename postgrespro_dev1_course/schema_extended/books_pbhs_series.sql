-- table connecting three realtions
create table books_pbhs_series (

	book_id integer not null references bookstore.books,
	pbh_id integer not null references bookstore.publishing_house,
	serie_id integer references bookstore.series

);
