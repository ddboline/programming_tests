#!/bin/bash

for DIR in scipy python numpy cython boost_python sqlalchemy sklearn scala;
do
    cd $DIR
    sh test_cloud9.sh
    cd ../
done
