#!/bin/bash

for DIR in scipy python3 numpy cython sqlalchemy ;
do
    cd $DIR
    sh setup_conda.sh
    cd ../
done
