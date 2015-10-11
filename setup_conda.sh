#!/bin/bash

for DIR in scipy python3 numpy cython sqlalchemy sklearn ;
do
    cd $DIR
    sh setup_conda.sh
    cd ../
done
