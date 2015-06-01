#!/bin/bash

sudo apt-get update
sudo apt-get install -y cython libgsl0-dev cython3

make clean
make
