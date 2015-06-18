#!/bin/bash

for DIR in cython;
do
    cd $DIR
    sh test_conda.sh
    cd ../
done
