#!/usr/bin/python

import os
from sqlalchemy import create_engine
import pandas as pd

def mysql_example():
    engine = create_engine( 'mysql://ddboline:BQGIvkKFZPejrKvX@localhost/world' )
    con = engine.connect()
    result = con.execute('show tables;')
    tables = []
    for row in result:
        tables.append( row[0] )

    table_dict = {}
    for table in tables:
        fields = []
        result = con.execute('describe %s;' % table)
        for row in result:
            fields.append( row[0] )
        table_dict[table] = fields
    
    # print table_dict
    
    dframes = {}
    
    for table , fields in table_dict.iteritems():
        query = 'select %s from %s;' % (', '.join(fields) , table )
        # print query
        result = con.execute(query)
        rows = result.fetchall()
        dframes[table] = pd.DataFrame( rows , columns=fields )
        # dframes[table] = pd.DataFrame( columns={ x[0]: x[1] for x in enumerate(fields)} )
    
    # for t , df in dframes.items():
        # print t
        # print df.columns
    # print dframes['Country']['Name']
    return dframes

if __name__ == '__main__':
    mysql_example()
