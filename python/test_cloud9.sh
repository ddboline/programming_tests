#!/bin/bash


nosetests unittests.py file_sync.py

./analyze_gmail.py temp.mbox
./default_dict_tree.py
echo multiprocessing `time ./stock_parser.py`
echo green `time ./stock_parser_green.py`
echo greenpool `time ./stock_parser_greenpool.py`
echo pool `time ./stock_parser_pool.py`
echo single `time ./stock_parser_single.py`
echo thread `time ./stock_parser_thread.py`
./sampling_vose_alias_method.py
