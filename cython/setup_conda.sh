#!/bin/bash

sudo apt-get update
sudo apt-get install -y cython libgsl0-dev cython3

sudo /opt/conda/bin/conda install --yes cython numba

make clean
make
