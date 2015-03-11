#!/bin/bash

# git clone https://github.com/ddboline/programming_tests.git

sudo apt-get install -y postgresql

sudo -u postgres createuser -E -e $USER
sudo -u postgres psql -c "CREATE ROLE $USER PASSWORD 'BQGIvkKFZPejrKvX' NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT LOGIN;" 
sudo -u postgres createdb mydb

for N in `seq 0 20`; 
do 
    psql mydb $USER < test${N}.sql ; 
done
