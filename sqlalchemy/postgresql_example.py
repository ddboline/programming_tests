#!/usr/bin/python

import os
from sqlalchemy import create_engine
import pandas as pd
from subprocess import Popen, PIPE, call

USER = os.getenv('USER')

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
    engine = create_engine('postgresql://%s:BQGIvkKFZPejrKvX@localhost/mydb' % USER)
    con = engine.connect()

    result = con.execute(postgresql_list_tables)
    tables = []
    for row in result:
        tables.append(row[1])

    table_dict = {}
    for table in tables:
        fields = []
        postgresql_describe_table = ''' select column_name, data_type, character_maximum_length
        from INFORMATION_SCHEMA.COLUMNS where table_name = '%s'; ''' % table

        result = con.execute(postgresql_describe_table)
        for row in result:
            fields.append(row[0])
        table_dict[table] = fields

    dframes = {}

    for table, fields in table_dict.items():
        query = 'select %s from %s;' % (', '.join(fields), table)
        # print(query)
        result = con.execute(query)
        rows = result.fetchall()
        dframes[table] = pd.DataFrame(rows, columns=fields)

    for t, df in dframes.items():
        df.to_csv('%s.csv' % t, index_label='Index')

    return dframes

#def postgresql_example_test():
#    engine = create_engine('postgresql://%s:BQGIvkKFZPejrKvX@localhost/mydb' % USER)
#    con = engine.connect()
#
#    result = con.execute(postgresql_list_tables)
#    tables = []
#    for row in result:
#        tables.append(row[1])
#
#    for table in tables:
#        df = pd.read_sql("SELECT * from %s" % table, engine)
#        df.to_csv('%s.csv' % (table), index_label='Index')

def test_postgresql_example():
    from util import get_md5
    postgresql_example()
    
    csv_md5 = {'booking.csv': '90fd6d84b6234ff73acc5208995cf85e',
               'contact.csv': 'b1d0f7c24d7ac5dfd70668c17c5e559d',
               'hobby.csv': '0b3fbf0ef6bcec8f2c5c68cc111931fd',
               'hobby_shadow.csv': 'a9919bc60b43b4fb092924ed1ad4df5a',
               'person.csv': 'fcb0b9c85213e0999eff0b197931f624',
               'person_hobby.csv': 'cb4bbd262f356c91d48d88009872f3c2',}

    for fn_, md5 in csv_md5.items():
        md5_ = get_md5(fn_)
        assert md5_ == md5


if __name__ == '__main__':
    postgresql_example()
    #postgresql_example_test()
