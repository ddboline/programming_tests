#!/bin/bash

sudo apt-get install -y make

make clean
make

cd cpp_socket
make clean
make
