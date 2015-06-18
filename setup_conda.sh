#!/bin/bash

for DIR in cython;
do
    cd $DIR
    sh setup_conda.sh
    cd ../
done
