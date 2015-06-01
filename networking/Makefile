CXX = gcc
CPP = g++

TARGETS = client client_udp server server_udp test

all: $(TARGETS)

%: %.c
	$(CXX) -Wall $*.c -o $* -lpthread

clean:
	rm $(TARGETS)
