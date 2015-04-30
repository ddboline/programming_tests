#!/bin/bash

for F in *.scala;
do
    echo $F
    scalac $F
done

for F in `ls *.scala | sed 's:.scala::g'`;
do
    echo $F
    scala $F
done
