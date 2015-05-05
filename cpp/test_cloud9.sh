#!/bin/bash

make clean
make
NUMBER=`head -c1000 /dev/urandom | tr -dc [:digit:] | head -c8`
echo atoi_impl $NUMBER
./atoi_impl $NUMBER
echo prbs7 $NUMBER
./prbs7 $NUMBER
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
