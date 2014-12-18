#!/usr/bin/python

import os
from sqlalchemy import create_engine
import pandas as pd

def postgresql_example():
    engine = create_engine( 'postgresql://ddboline@localhost/mydb' )
    con = engine.connect()
    
    dat = pd.read_sql( 'select * from person' , con )
    
    print dat

if __name__ == '__main__':
    postgresql_example()
