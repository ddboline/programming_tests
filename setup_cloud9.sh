#!/bin/bash

for DIR in scipy python numpy postgresql mysql cython boost_python sqlalchemy;
do
    cd $DIR
    sh setup_cloud9.sh
    cd ../
done

