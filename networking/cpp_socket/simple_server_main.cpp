#include "ServerSocket.hpp"
#include "SocketException.hpp"
#include <string>
#include <iostream>

int main ( int argc, char ** argv ) {
    std::cout << "running....\n";
    int port = 30000;
    if(argc > 1) {
        try {
            port = std::stoi(std::string(argv[1]));
        }
        catch(...) {};
    }
    std::cout << port << std::endl;
    try {
        // Create the socket
        ServerSocket server ( port );
        while ( true ) {
            ServerSocket new_sock;
            server.accept ( new_sock );
            try {
                while ( true ) {
                    std::string data;
                    new_sock >> data;
                    new_sock << data;
                    std::cout << "data " << data << std::endl;
                }
            }
            catch ( SocketException& ) {};
        }
    }
    catch ( SocketException& e ) {
    std::cout << "Exception was caught:" << e.description() << "\nExiting.\n";
    }
    return 0;
}
