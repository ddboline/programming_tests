#!/bin/bash

for DIR in scipy python3 numpy cython;
do
    cd $DIR
    sh test_conda.sh
    cd ../
done
