#!/bin/bash

make
cd cpp_socket
make
cd ..

PORT=`shuf -i 2000-65000 -n 1`
./server.py $PORT &
PROC=$!
sleep 5
./client.py localhost $PORT "Passed python port: $PORT"

PORT=`shuf -i 2000-65000 -n 1`
./server $PORT &
PROC="${PROC} $!"
sleep 5
echo "Passed c port: $PORT" | ./client localhost $PORT

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
./simple_client $PORT "Passed c++ port: $PORT"

sleep 10
kill -9 ${PROC}
make clean

cd cpp_socket
make clean
cd ..
