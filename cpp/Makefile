CXX = gcc
CPP = g++

BOOST_INC = /usr/include
BOOST_LIB = /usr/lib

CXX_FILES = reverse_string atoi_impl ternary_conditional pthread_hello prbs7_c threadadd
CPP_FILES = async_test doubly_linked_list forward functional inheritance inheritance_test move packaged_task parse_csv prbs7 primes remove_char_inplace sampling_vose_alias_method selection_sort split_string thread_add thread_hello double_free

%: %.c
	$(CXX) -Wall -O3 -g3 $*.c -o $* -lpthread

%: %.cpp
	$(CPP) -Wall -pthread -std=c++11 -O3 -g3 -I$(BOOST_INC) -fPIC -L$(BOOST_LIB) $*.cpp -o $*

all: $(CXX_FILES) $(CPP_FILES)

clean:
	rm $(CXX_FILES) $(CPP_FILES)
