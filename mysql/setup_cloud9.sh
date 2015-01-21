#!/bin/bash

# git clone https://github.com/ddboline/programming_tests.git

sudo apt-get install -y mysql-server

sudo mysql_install_db
sudo /usr/bin/mysql_secure_installation

for N in `seq 0 20`;
do
    mysql --user=$USER --password=BQGIvkKFZPejrKvX mydb < ../postgresql/test${N}.sql;
done

