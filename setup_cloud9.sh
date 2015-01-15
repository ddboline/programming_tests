#!/bin/bash

for DIR in scipy python numpy postgresql mysql cython boost_python sqlalchemy;
do
    sh setup_cloud9.sh
done

