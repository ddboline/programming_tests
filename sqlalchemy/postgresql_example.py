#!/usr/bin/python

import os
from sqlalchemy import create_engine
import pandas as pd

def postgresql_example():
    engine = create_engine( 'postgresql://ddboline:BQGIvkKFZPejrKvX@localhost/mydb' )

    dat = pd.read_sql_query( 'select * from person' , engine )
    
    print dat

if __name__ == '__main__':
    postgresql_example()
