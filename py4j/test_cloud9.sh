#!/bin/bash

for F in *.scala;
do
    echo $F
    scalac -classpath /usr/share/py4j/py4j0.8.2.1.jar $F
done

scala -classpath /usr/share/py4j/py4j0.8.2.1.jar Py4j 2>&1 > /dev/null &
PROC=$!

sleep 5

python test_py4j.py

PROC2=`ps -eF | grep scala | grep Py4j | awk '{print $2}'`
echo $PROC $PROC2
kill -9 $PROC $PROC2
