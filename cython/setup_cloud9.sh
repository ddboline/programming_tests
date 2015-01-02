#!/bin/bash

sudo apt-get install -y cython libgsl0-dev

python setup.py build_ext --inplace

./run_basel.py
./run_chudnovsky.py
./run_cos.py
./run_fibonacci.py
./run_integ.py
./run_integral_approx.py 
./run_matmul.py 100 100 100
./run_pi_wallis.py 
