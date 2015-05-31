CXX = gcc
CPP = g++

BOOST_INC = /usr/include
BOOST_LIB = /usr/lib

CXX_FILES = reverse_string atoi_impl ternary_conditional pthread_hello
CPP_FILES = prbs7 selection_sort sampling_vose_alias_method primes thread_hello forward

%: %.c
	$(CXX) -Wall -O3 $*.c -o $* -lpthread

%: %.cpp
	$(CPP) -Wall -pthread -std=c++11 -O3 -I$(BOOST_INC) -fPIC -L$(BOOST_LIB) $*.cpp -o $*

all: $(CXX_FILES) $(CPP_FILES)

clean:
	rm $(CXX_FILES) $(CPP_FILES)
