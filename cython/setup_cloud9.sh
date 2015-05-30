#!/bin/bash

sudo apt-get update
sudo apt-get install -y cython libgsl0-dev cython3

python3 setup.py build_ext --inplace
