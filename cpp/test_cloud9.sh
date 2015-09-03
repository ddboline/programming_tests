#!/bin/bash

make
NUMBER=`head -c1000 /dev/urandom | tr -dc [:digit:] | head -c8`
echo atoi_impl $NUMBER
./atoi_impl $NUMBER
echo prbs7 $NUMBER
./prbs7 $NUMBER
echo prbs7_c $NUMBER
./prbs7_c $NUMBER
echo reverse_string HelloWorld
./reverse_string HelloWorld
echo selection_sort $NUMBER
./selection_sort $NUMBER
echo ternary_conditional
./ternary_conditional
echo sampling_vose_alias_method
./sampling_vose_alias_method
echo primes
./primes 1000
echo thread_hello
./thread_hello
echo threadadd
./threadadd
echo thread_add
./thread_add
echo pthread_hello
./pthread_hello
echo async_test
./async_test
echo doubly_linked_list
./doubly_linked_list
echo forward
./forward
echo functional
./functional
echo inheritance
./inheritance
echo inheritance_test
./inheritance_test
echo move
./move
echo packaged_task
./packaged_task
echo parse_csv
./parse_csv
echo remove_char_inplace HelloWorld
./remove_char_inplace HelloWorld
echo split_string
./split_string
make clean
