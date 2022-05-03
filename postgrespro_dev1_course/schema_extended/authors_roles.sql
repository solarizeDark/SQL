create table authors_roles (

	author_id integer not null references bookstore.authors,
	role_id integer not null references bookstore.roles,

	constraint authors_roles_pk primary key(author_id, role_id)

);
