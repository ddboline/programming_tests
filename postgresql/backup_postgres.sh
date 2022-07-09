#!/bin/bash

DATABASES="
auth_server_rust
aws_app_cache
calendar_app_cache
diary_app_cache
garmin_summary
movie_queue
podcatch
postgres
security_logs
sync_app_cache
"

for DB in $DATABASES;
do
    echo $DB
    sudo -u postgres pg_dump ${DB} | gzip > ${DB}.sql.gz
done
