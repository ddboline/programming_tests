CXX = gcc
CPP = g++

all: client client_udp server server_udp telnet telnet_test test threadadd udp_talker

client:
	$(CXX) ./client.c -o ./client

client_udp:
	$(CXX) ./client_udp.c -o ./client_udp

server:
	$(CXX) ./server.c -o ./server

server_udp:
	$(CXX) ./server_udp.c -o ./server_udp

telnet:
	$(CXX) ./telnet.c -o ./telnet -lpthread

telnet_test:
	$(CXX) ./telnet_test.c -o ./telnet_test -lpthread

test:
	$(CXX) ./test.c -o ./test

threadadd:
	$(CXX) ./threadadd.c -o ./threadadd -lpthread

udp_talker:
	$(CXX) ./udp_talker.c -o ./udp_talker

clean:
	rm ./client ./client_udp ./server ./server_udp ./telnet ./telnet_test ./test ./threadadd ./udp_talker
