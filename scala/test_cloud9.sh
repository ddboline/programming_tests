#!/bin/bash

make

for F in `ls *.scala | sed 's:.scala::g'`;
do
    echo $F
    scala $F
done

make clean
