#!/bin/bash

sudo apt-get install -y cython libgsl0-dev

python setup.py build_ext --inplace

echo "Basel"
./run_basel.py
echo "Chudnovsky"
./run_chudnovsky.py
echo "Cosine"
./run_cos.py
echo "Fibonacci"
./run_fibonacci.py
echo "Integral"
./run_integ.py
echo "Integral Approx"
./run_integral_approx.py 
echo "Matrix Multiplication"
./run_matmul.py 100 100 100
echo "Pi Wallis"
./run_pi_wallis.py 
