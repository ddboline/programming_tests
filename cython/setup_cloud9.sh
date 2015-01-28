#!/bin/bash

sudo apt-get install -y cython libgsl0-dev

python setup.py build_ext --inplace
