#!/usr/bin/python

import os
from sqlalchemy import create_engine
import pandas as pd

def read_hpodder():
    engine = create_engine('sqlite:///hpodder.db', echo=True)
    con = engine.connect()
    result = con.execute("select * from podcasts limit 10;")
    for line in result:
        print line
    return

if __name__ == '__main__':
    read_hpodder()
