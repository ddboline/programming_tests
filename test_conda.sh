#!/bin/bash

for DIR in scipy python3 cython;
do
    cd $DIR
    sh test_conda.sh
    cd ../
done
