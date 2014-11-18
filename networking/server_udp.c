/* A simple server in the internet domain using TCP
   The port number is passed as an argument */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>

void error(const char *msg)
{
    perror(msg);
    exit(1);
}

int main(int argc, char *argv[])
{
     int sockfd, newsockfd, portno;
     socklen_t clilen;
     char buffer[1024];
     struct sockaddr_in serv_addr, cli_addr;
     int n , saddrlen = sizeof(serv_addr);
     if (argc < 2) {
         fprintf(stderr,"ERROR, no port provided\n");
         exit(1);
     }
     sockfd = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
     if (sockfd < 0) 
        error("ERROR opening socket");
     memset( &serv_addr , 0 , sizeof(serv_addr) );
     portno = atoi(argv[1]);
     serv_addr.sin_family = AF_INET;
     serv_addr.sin_addr.s_addr = INADDR_ANY;
     serv_addr.sin_port = htons(portno);
     
     if( bind( sockfd, (struct sockaddr *) &serv_addr, sizeof(serv_addr) ) < 0 ) error("ERROR on binding");
     
     while(1) {
        memset(buffer,0,1024);
        
        n = recvfrom( sockfd , buffer , 1024 , 0 , (struct sockaddr *) &serv_addr , &saddrlen );
        if( n<0 ) error("ERROR reading from socket");
        printf( "message %s\n" , buffer );
     }
     
     close(sockfd);
     return 0; 
}
