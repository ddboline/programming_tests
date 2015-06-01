# Makefile for the socket programming example
#
simple_server_objects = ServerSocket.o Socket.o simple_server_main.o
simple_client_objects = ClientSocket.o Socket.o simple_client_main.o


all : simple_server simple_client

%.o: %.cpp
	g++ -std=c++11 -c $*.cpp

simple_server: $(simple_server_objects)
	g++  -std=c++11 -o simple_server $(simple_server_objects)


simple_client: $(simple_client_objects)
	g++ -std=c++11 -o simple_client $(simple_client_objects)

clean:
	rm -f *.o simple_server simple_client
