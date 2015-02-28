#!/bin/bash

# git clone https://github.com/ddboline/programming_tests.git

sudo apt-get install -y mysql-server

sudo mysql_install_db
sudo /usr/bin/mysql_secure_installation

sudo mysql --user=root mysql --execute="CREATE USER 'ddboline'@'%' IDENTIFIED BY 'BQGIvkKFZPejrKvX';"
sudo mysql --user=root mysql --execute="GRANT ALL PRIVILEGES ON *.* TO 'ddboline'@'%' WITH GRANT OPTION;"

mysql --user=$USER --password=BQGIvkKFZPejrKvX --execute="CREATE DATABASE IF NOT EXISTS mydb"

for N in `seq 0 20`;
do
    mysql --user=$USER --password=BQGIvkKFZPejrKvX mydb < ../postgresql/test${N}.sql;
done

