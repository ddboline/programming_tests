#!/bin/bash

for DIR in scipy python3 numpy cython boost_python sqlalchemy sklearn;
do
    cd $DIR
    sh test_python3.sh
    cd ../
done
