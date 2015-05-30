PYTHON_VERSION = 3.4
PYTHON_VER = 34
PYTHON_INCLUDE = /usr/include/python$(PYTHON_VERSION)

# location of the Boost Python include files and library
BOOST_INC = /usr/include
BOOST_LIB = /usr/lib

# compile mesh classes
TARGET = hello_ext

LDFLAGS = $(shell python$(PYTHON_VERSION)-config --ldflags)

$(TARGET).so: $(TARGET).o
	g++ -shared -Wl,--export-dynamic $(TARGET).o -L$(BOOST_LIB) -lboost_python-py$(PYTHON_VER) $(LDFLAGS) -o $(TARGET).so
$(TARGET).o: $(TARGET).cpp
	g++ -I$(PYTHON_INCLUDE) -I$(BOOST_INC) -fPIC -c $(TARGET).cpp

clean:
	rm *.o *.so
