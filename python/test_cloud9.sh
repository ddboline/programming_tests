#!/bin/bash

nosetests unittests.py analyze_gmail.py file_sync.py exversion.py parse_email.py util.py

./analyze_gmail.py temp.mbox
./default_dict_tree.py
./duck_method.py
./exversion.py
./inheritance_test.py
./inplace_remove.py
./lambda_gamma_functions.py
./liveblogging_list.py
./parse_email.py temp.mbox

# echo multiprocessing 
# time ./stock_parser.py
# echo green 
# time ./stock_parser_green.py
# echo greenpool 
# time ./stock_parser_greenpool.py
# echo pool 
# time ./stock_parser_pool.py
# echo single 
# time ./stock_parser_single.py
# echo thread 
# time ./stock_parser_thread.py
./sampling_vose_alias_method.py
