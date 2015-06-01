#include "ClientSocket.hpp"
#include "SocketException.hpp"
#include <iostream>
#include <string>

int main ( int argc, char ** argv ) {
    int port = 30000;
    std::string message;
    if(argc > 1) {
        try {
            port = std::stoi(std::string(argv[1]));
        }
        catch(...) {};
        for(int idx=1; idx<argc; idx++){
            message += std::string(argv[idx]);
            message += " ";
        }
    }
    try {
        ClientSocket client_socket ( "localhost", port );
        std::string reply;
        try {
            if(message.size() == 0) {
                client_socket << "Test message.";
                client_socket >> reply;
            }
            else {
                client_socket << message;
                client_socket >> reply;
            }
        }
        catch ( SocketException& ) {};
        std::cout << "We received this response from the server:\n\"" << reply << "\"\n";;
    }
    catch ( SocketException& e ) {
        std::cout << "Exception was caught:" << e.description() << "\n";
    }
    return 0;
}
