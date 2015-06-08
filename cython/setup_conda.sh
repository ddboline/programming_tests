#!/bin/bash

sudo apt-get update
sudo apt-get install -y libgsl0-dev make gcc g++

sudo /opt/conda/bin/conda install --yes cython numba

make clean
make
