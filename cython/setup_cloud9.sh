#!/bin/bash

sudo apt-get update
sudo apt-get install -y cython libgsl0-dev

make clean
make
make python
