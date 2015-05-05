CXX = gcc
CPP = g++

all: reverse_string atoi_impl ternary_conditional prbs7 selection_sort sampling_vose_alias_method primes

reverse_string:
	$(CXX) -O3 ./reverse_string.c -o ./reverse_string

atoi_impl:
	$(CXX) -O3 ./atoi_impl.c -o ./atoi_impl

ternary_conditional:
	$(CXX) -O3 ./ternary_conditional.c -o ./ternary_conditional

prbs7:
	$(CXX) -O3 ./prbs7.c -o ./prbs7

selection_sort:
	$(CPP) -O3 ./selection_sort.cpp -o ./selection_sort

sampling_vose_alias_method:
	$(CPP) -std=c++11 -O3 ./sampling_vose_alias_method.cpp -o ./sampling_vose_alias_method

primes:
	$(CPP) -O3 ./primes.cpp -o ./primes

clean:
	rm ./reverse_string ./atoi_impl ./ternary_conditional ./prbs7 ./selection_sort ./sampling_vose_alias_method ./primes
