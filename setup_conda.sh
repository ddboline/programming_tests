#!/bin/bash

for DIR in scipy cython;
do
    cd $DIR
    sh setup_conda.sh
    cd ../
done
