/*
 *-
 *-   Purpose and Methods: Implement a simple UDP talker/receiver. Created from
 *-       d0dad_client
 *-
 *-   Inputs  :
 *-   Outputs :
 *-   Controls:
 *-
 *-   
 *-
*/
#define STANDALONE  /* Make a "main" routine. */
/* #define IP_BY_NUMBER */

#define MAX_PACKET_SIZE 1024

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>
#define ERROR_NUMBER errno
#define SLEEP sleep
#define PRINTF printf
#define SOCKADDR struct sockaddr

#include <signal.h>
#include <string.h>

void fatal_error(const char *text, const int errcode)
{
  PRINTF("%s: %d\n",text,errcode);
  exit(errcode);
}

void runTalker(int argc, char ** argv, char ** envp)
{
  int i,s,error,s_len,s_myLen,port,retcode,inout,delaysecs;
  struct sockaddr_in s_address,s_myAddress;
  struct hostent *hptr, *hptrMe;
  char ipaddr[4] = {127,0,0,1};
  char mode[255],remote_name[255],command[1024],message[256],myname[1024];
  char *heartbeat;
  delaysecs=2;

  heartbeat = "HEARTBEAT";

  /* Parse command line information. */
  if( argc!=4 ) {
    PRINTF("usage: udp_talker mode node_name port_number\n");
    PRINTF("   mode = \"echo\", \"echo1\", \"send\", \"listen\"\n");
    PRINTF("Command line: ");
    for( i=0 ; i<argc ; i++ ) PRINTF(" %s\n",argv[i]);
    PRINTF("\n");
    fatal_error("Invalid command line\n",1);
  }
  sscanf(argv[1],"%s",mode);        
  sscanf(argv[2],"%s",remote_name);
  sscanf(argv[3],"%d",&port);

  hptrMe=gethostbyaddr(ipaddr,4,AF_INET);

  if( !(int)hptrMe ) fatal_error("Could not translate hostname",ERROR_NUMBER);
  PRINTF("My address is "); for( i=0 ; i<4 ; i++ ) PRINTF("%d.",(unsigned char)(hptrMe->h_addr_list[0][i])); PRINTF("\n");
  s_myAddress.sin_family=AF_INET;
  s_myAddress.sin_port=htons((unsigned short)port);
  bcopy(hptrMe->h_addr,(char *)&s_myAddress.sin_addr,hptrMe->h_length);
  s_myLen = sizeof(s_myAddress);
  
  /* and then do the same for the remote system */
  hptr=gethostbyname(remote_name);
  if( !(int)hptr ) fatal_error("Could not translate hostname",ERROR_NUMBER);
  s_address.sin_family=AF_INET;
  s_address.sin_port=htons((unsigned short)port);
  /*s_address.sin_addr.s_addr=INADDR_ANY;*/
  bcopy(hptr->h_addr,(char *)&s_address.sin_addr,hptr->h_length);
  s_len = sizeof(s_address);

  /* Allocate a socket and make connection. */
  s=socket(PF_INET,SOCK_DGRAM,IPPROTO_UDP);
  if( s==(-1) ) fatal_error("udp_talker, socket open",ERROR_NUMBER);
  error=bind(s,(struct sockaddr *)&s_myAddress,sizeof(s_myAddress));
  if( error!=0 ) fatal_error("udp_talker, bind",ERROR_NUMBER);

  /* This kicks off a single packet which is rotated around via the echo.
     For this mode, the other system must be in "echo" and be started first. */
  if( !strcmp(mode,"echo1") ) {
    sprintf(command,"%s 1\n",heartbeat);
    PRINTF("Starting rotation of %s",command);
    s_len = sendto(s,command,strlen(command),0,(SOCKADDR*)&s_address,sizeof(s_address));
    s_len=1024;
    SLEEP(delaysecs);
  }

  /* Data processing, either sending or an echo of the input... */
  i=1;
  inout=sizeof(s_address);
  while( 1 ) {
    /* Echo mode. Read first, then send. */
    if( !strcmp(mode,"echo") || !strcmp(mode,"echo1") ) {
      s_len = MAX_PACKET_SIZE;
      s_len=recvfrom(s,command,s_len,0,(SOCKADDR*)&s_address,&inout);
      if( s_len<0 ) {
        sprintf(command,"Client: Error %d on read\n",ERROR_NUMBER);
        perror(command);
        exit(ERROR_NUMBER);
      }

      if( !strcmp(mode,"echo1") ) sprintf(command,"%s %d\n",heartbeat,i++);
      else command[s_len]='\0';
      PRINTF("Echoing: %s",command);
      s_len = sendto(s,command,strlen(command),0,(SOCKADDR*)&s_address,sizeof(s_address));
      SLEEP(delaysecs);
    }
    else if( !strcmp(mode,"send") ) { /* Sender mode */
      sprintf(command,"%s %d",heartbeat,i++);
      PRINTF("%s\n",command);
      s_len = sendto(s,command,strlen(command),0,(SOCKADDR*)&s_address,sizeof(s_address));
      s_len=1024;
      SLEEP(delaysecs);
    }
    else if( !strcmp(mode,"listen") ) {
      s_len = MAX_PACKET_SIZE;
      s_len=recvfrom(s,command,s_len,0,(SOCKADDR*)&s_address,&inout);
      if( s_len<0 ) {
        sprintf(command,"Client: Error %d on read\n",ERROR_NUMBER);
        perror(command);
        exit(ERROR_NUMBER);
      }
      else PRINTF("Received packet: %s\n",command);
	/*PRINTF("Received packet %d (size=%d)\n",i++,s_len); */
    }
    else {
      sprintf(command,"Unknown mode = %s\n",mode);
      fatal_error(command,2);
    }
  }

  close(s);
  exit(0);
}

#ifdef STANDALONE
int main(int argc, char ** argv, char ** envp)
{
  runTalker(argc,argv,envp);
  return 0;
}
#endif
