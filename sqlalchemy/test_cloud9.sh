#!/bin/bash

rm test.db
py.test postgresql_example.py util.py
./sqlite_test.py
./sqlite_example.py

scp ddboline@home.ddboline.net:/home/ddboline/setup_files/build/programming_tests/sqlalchemy/hpodder.db .
./read_hpodder.py
