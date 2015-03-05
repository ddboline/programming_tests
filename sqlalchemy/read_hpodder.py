#!/usr/bin/python

import os
from sqlalchemy import create_engine
import pandas as pd

def read_hpodder():
    engine = create_engine('sqlite:///hpodder.db', echo=False)
    con = engine.connect()

    for line in con.execute("select * from sqlite_master where type='table';"):
        if 'CREATE TABLE' in line[4]:
                print line[4].replace(',', ',\n')
    
    for line in con.execute("select name from sqlite_master where type='table';"):
        print line
    
    for line in con.execute("select feedurl from podcasts;"):
        print line

    result = con.execute("select epurl, status from episodes limit 10;")
    for line in result:
        print line

    return

if __name__ == '__main__':
    read_hpodder()
