#!/bin/bash

DATABASES="
bucardo
florida_doc_inmate_info
mydb
postgres
recipes
texas_high_value_datasets

aws_app_cache
diary_app_cache
calendar_app_cache
garmin_summary
movie_queue
podcatch
rust_auth_server
security_logs
ssh_intrusion_logs
sync_app_cache
"

for DB in $DATABASES;
do
    echo $DB
    sudo -u postgres pg_dump ${DB} | gzip > ${DB}.sql.gz
done
