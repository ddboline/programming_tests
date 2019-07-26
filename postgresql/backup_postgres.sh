#!/bin/bash

DATABASES="
bucardo
florida_doc_inmate_info
garmin_summary
movie_queue
mydb
podcatch
postgres
recipes
rust_auth_server
security_logs
ssh_intrusion_logs
sync_app_cache
texas_high_value_datasets
"

for DB in $DATABASES;
do
    echo $DB
    sudo -u postgres pg_dump ${DB} | gzip > ${DB}.sql.gz
done
