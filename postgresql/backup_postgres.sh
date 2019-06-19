#!/bin/bash

DATABASES="
florida_doc_inmate_info
garmin_summary
movie_queue
mydb
podcatch
postgres
recipes
ssh_intrusion_logs
texas_high_value_datasets
rust_auth_server
sync_app_cache
"

for DB in $DATABASES;
do
    echo $DB
    sudo -u postgres pg_dump ${DB} | gzip > ${DB}.sql.gz
done
