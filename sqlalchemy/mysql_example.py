#!/usr/bin/python
# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
import pandas as pd

def mysql_example(database):
    engine = create_engine('mysql://ddboline:BQGIvkKFZPejrKvX@localhost/%s' % database)
    con = engine.connect()
    result = con.execute('show tables;')
    tables = []
    for row in result:
        tables.append(row[0])

    table_dict = {}
    for table in tables:
        fields = []
        result = con.execute('describe %s;' % table)
        for row in result:
            fields.append(row[0])
        table_dict[table] = fields

    # print(table_dict)

    dframes = {}

    for table, fields in table_dict.iteritems():
        query = 'select %s from %s;' % (', '.join(fields), table)
        # print(query)
        result = con.execute(query)
        rows = result.fetchall()
        dframes[table] = pd.DataFrame(rows, columns=fields)

    for t, df in dframes.items():
        df.to_csv('%s_%s.csv' % (database, t), index_label='Index')

    return dframes

def mysql_example_test(database):
    engine = create_engine('mysql://ddboline:BQGIvkKFZPejrKvX@localhost/%s' % database)
    con = engine.connect()

    result = con.execute('show tables;')
    tables = []
    for row in result:
        tables.append(row[0])

    table_dict = {}
    for table in tables:
        df = pd.read_sql("SELECT * from %s" % table, engine)
        df.to_csv('%s_%s.csv' % (database, table), index_label='Index')

if __name__ == '__main__':
    mysql_example_test('world')
    mysql_example_test('mydb')
