#!/bin/bash

sudo apt-get update
sudo apt-get install -y cython3 libgsl0-dev

make clean
make
