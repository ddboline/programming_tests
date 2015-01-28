#!/bin/bash

./analyze_gmail.py temp.mbox
./default_dict_tree.py
./file_sync.py
./stock_parser.py
