#!/usr/bin/python

import os
from sqlalchemy import create_engine
import pandas as pd

postgresql_list_tables = '''
SELECT n.nspname as "Schema",
  c.relname as "Name",
  CASE c.relkind WHEN 'r' THEN 'table' WHEN 'v' THEN 'view' WHEN 'm' THEN 'materialized view' WHEN 'i' THEN 'index' WHEN 'S' THEN 'sequence' WHEN 's' THEN 'special' WHEN 'f' THEN 'foreign table' END as "Type",
  pg_catalog.pg_get_userbyid(c.relowner) as "Owner"
FROM pg_catalog.pg_class c
     LEFT JOIN pg_catalog.pg_namespace n ON n.oid = c.relnamespace
WHERE c.relkind IN ('r','')
      AND n.nspname <> 'pg_catalog'
      AND n.nspname <> 'information_schema'
      AND n.nspname !~ '^pg_toast'
  AND pg_catalog.pg_table_is_visible(c.oid)
ORDER BY 1,2;
'''

def postgresql_example():
    engine = create_engine( 'postgresql://ddboline:BQGIvkKFZPejrKvX@localhost/mydb' )
    con = engine.connect()

    result = con.execute(postgresql_list_tables)
    tables = []
    for row in result:
        tables.append( row[1] )
    
    for table in tables:
        postgresql_describe_table = ''' select column_name, data_type, character_maximum_length
        from INFORMATION_SCHEMA.COLUMNS where table_name = '%s'; ''' % table
        
        result = con.execute(postgresql_describe_table)
        for row in result:
            # print row
            print '%s.%s' % ( table , row[0] ) , row[1:]

if __name__ == '__main__':
    postgresql_example()
