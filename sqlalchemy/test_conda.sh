#!/bin/bash

rm test.db
nosetests postgresql_example.py util.py
python3 ./sqlite_test.py
python3 ./sqlite_example.py

scp ddboline@ddbolineathome.mooo.com:/home/ddboline/setup_files/build/programming_tests/sqlalchemy/hpodder.db .
python3 ./read_hpodder.py
