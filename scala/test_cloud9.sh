#!/bin/bash

for F in *.scala;
do
    BASENAME=`echo $F | sed 's:.scala::g'`
    echo $F $BASENAME
    scalac $F
    scala $BASENAME
done
