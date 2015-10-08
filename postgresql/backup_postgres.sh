#!/bin/bash

DATABASES="
florida_doc_inmate_info
garmin_summary
lahman2014
mydb
podcatch
postgres
quassel
ssh_intrusion_logs
texas_high_value_datasets
"

for DB in $DATABASES;
do
    echo $DB
    pg_dump ${DB} | gzip > ${DB}.sql.gz
done
