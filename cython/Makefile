CXX = gcc
CPP = g++

all: integ primes smith_number sampling_vose_alias_method python

%: %.c
	$(CXX) -O3 $*.c -o $*

%: %.cpp
	$(CPP) -std=c++11 -O3 $*.cpp -o $*

clean:
	rm -rf cos_func.c matmul2.c matmul3.c primes primes1.cpp sampling_vose_alias_method sampling_vose_alias_method1.cpp smith_number smith_number2.cpp __pycache__ *.so *.pyc build

python:
	python3 setup.py build_ext --inplace