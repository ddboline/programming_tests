#!/bin/bash

for DIR in scipy python numpy cython boost_python sqlalchemy scipy;
do
    cd $DIR
    sh setup_cloud9.sh
    cd ../
done

