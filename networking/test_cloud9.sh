#!/bin/bash

PORT=`shuf -i 2000-65000 -n 1`
./server.py $PORT &
PROC=$!
sleep 5
./client.py localhost $PORT "HEY THERE"

PORT=`shuf -i 2000-65000 -n 1`
./server $PORT &
PROC="${PROC} $!"
sleep 5
echo "HOW GOES IT" | ./client.py localhost $PORT

PORT=`shuf -i 2000-65000 -n 1`
./server_udp $PORT &
PROC="${PROC} $!"
sleep 5
./client_udp localhost $PORT &
PROC="${PROC} $!"

cd cpp_socket
PORT=`shuf -i 2000-65000 -n 1`
./simple_server $PORT &
PROC="${PROC} $!"
sleep 5
./simple_client $PORT "WHAT UP"

sleep 10
kill -9 ${PROC}
