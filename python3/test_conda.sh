#!/bin/bash

nosetests unittests.py analyze_gmail.py file_sync.py exversion.py parse_email.py

./analyze_gmail.py temp.mbox
./default_dict_tree.py
./file_sync.py
# ./stock_parser.py
./sampling_vose_alias_method.py
