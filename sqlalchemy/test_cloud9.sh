#!/bin/bash

rm test.db
nosetests postgresql_example.py util.py
./sqlite_test.py
./sqlite_example.py

scp ddboline@ddbolineathome.mooo.com:/home/ddboline/setup_files/build/programming_tests/sqlalchemy/hpodder.db .
./read_hpodder.py
