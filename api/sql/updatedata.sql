

delete from role_menu where menu=6  and role_id=1;
delete from role_menu where menu=7  and role_id=1;
delete from role_menu where menu=8  and role_id=1;

delete from role_menu where menu=26 and role_id=3;
delete from role_menu where menu=28 and role_id=3;
delete from role_menu where menu=29 and role_id=3;

insert into role(id, name, title, deleted) values (104, "PARENT", "ولی دانش آموز", 0 );

insert into role_menu(role_id, menu) VALUES (104, 1);
insert into role_menu(role_id, menu) VALUES (104, 20);
insert into role_menu(role_id, menu) VALUES (104, 21);
insert into role_menu(role_id, menu) VALUES (104, 22);
insert into role_menu(role_id, menu) VALUES (104, 23);
insert into role_menu(role_id, menu) VALUES (104, 34);
insert into role_menu(role_id, menu) VALUES (104, 35);
insert into role_menu(role_id, menu) VALUES (104, 25);
