#!/bin/bash

rm test.db
py.test postgresql_example.py util.py
python3 ./sqlite_test.py
python3 ./sqlite_example.py

scp ddboline@home.ddboline.net:/home/ddboline/setup_files/build/programming_tests/sqlalchemy/hpodder.db .
python3 ./read_hpodder.py
