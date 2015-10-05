#!/bin/bash

DATABASES="
florida_doc_inmate_info
garmin_summary
lahman2014
mydb
postgres
quassel
ssh_intrusion_logs
texas_high_value_datasets
"

for DB in $DATABASES;
do
    pg_dump ${DB} | gzip > ${DB}.sql.gz
done