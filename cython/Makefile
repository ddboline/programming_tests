CXX = gcc
CPP = g++

TARGETS = integ primes smith_number sampling_vose_alias_method

all: $(TARGETS)

%: %.c
	$(CXX) -O3 $*.c -o $*

%: %.cpp
	$(CPP) -std=c++11 -O3 $*.cpp -o $*

python:
	./setup.py build_ext --inplace

python3:
	python3 setup.py build_ext --inplace

clean:
	rm -rf cos_func.c matmul2.c matmul3.c primes1.cpp sampling_vose_alias_method1.cpp smith_number2.cpp __pycache__ *.so *.pyc build
	rm $(TARGETS)
