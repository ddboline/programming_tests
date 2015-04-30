#!/bin/bash

for F in *.scala;
do
    BASENAME=`echo $F | sed 's:.scala::g'`
    scalac $F
    scala $BASENAME
done
