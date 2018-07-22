use mysql;
update user set authentication_string=password(''), plugin='mysql_native_password' where user='root';
