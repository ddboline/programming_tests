#!/bin/bash

make clean
make
NUMBER=`head -c1000 /dev/urandom | tr -dc [:digit:] | head -c8`
echo $NUMBER
./atoi_impl $NUMBER
./prbs7
./reverse_string HelloWorld
./selection_sort
./ternary_conditional
