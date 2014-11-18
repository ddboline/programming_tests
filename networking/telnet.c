#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

#include <unistd.h>
#include <sys/types.h> 
#include <sys/socket.h>
#include <netinet/in.h>


#define NTELNETCOMMANDS 6
#define NTELNETTOKENS 20

typedef unsigned   char    u8_t;
typedef signed     char    s8_t;
typedef unsigned   short   u16_t;
typedef signed     short   s16_t;
typedef unsigned   long    u32_t;
typedef signed     long    s32_t;
typedef unsigned   long long    u64_t;
typedef signed     long long    s64_t;

pthread_mutex_t lock;
u8_t u8_array[4] = { 0x12 , 0x34 , 0x56 , 0x78 };
u16_t u16_array[4] = { 0x1234 , 0x5678 , 0x9abc , 0xdef0 };
u32_t u32_array[2] = { 0x12345678 , 0x9abcdef0 };

int lwip_send(int s, const void *data, size_t size, int flags)
{
    char output_buf[size+1];
    memset(output_buf,0,size+1);
    sprintf( output_buf , "%s" , (const char*)data );
    printf( "%s\n" , output_buf );
    return write(s,output_buf,strlen(output_buf));
}

int telnet_response(int s, const void *data, size_t size, int sockfd)
{
    int RECV_BUF_SIZE = 2048;
    int cidx;
    char input_buf[RECV_BUF_SIZE];
    
    memset( input_buf , 0 , size+1 );
    strcpy( input_buf , data );
    
    char *commands[NTELNETCOMMANDS] = { "mwr" , "mrd" , "stop" , "con" , "debug" , "initclk" };

    char * temp_str , ** pEnd = NULL;
    typedef enum { MWR = 0 , MRD = 1 , STOP = 2 , CON = 3 , DEBUG = 4 , INITCLK = 5 } command_type_t;
    command_type_t command_type = MWR;

    char tokens[NTELNETTOKENS][20] = {};

    temp_str = strtok( input_buf , " ");
    int number_tokens = 0;
    while( temp_str != NULL ) {
        strncpy( tokens[number_tokens] , temp_str , strlen( temp_str ) );
        ++number_tokens;
        temp_str = strtok( NULL , " {}\r\n");
    }

    for( cidx = 0 ; cidx < NTELNETCOMMANDS ; ++cidx ) {
        if( !strncmp( commands[cidx] , tokens[0] , strlen(commands[cidx]) ) )
            command_type = cidx;
    }

    if( command_type == STOP ) {
        close(s);
        close(sockfd);
        exit(0);
    }
    
    typedef enum { N=-1 , W = 0 , H = 1 , B = 2 } wtype_t;
    wtype_t wtype = N;
    char *wtypes[3] = { "w" , "h" , "b" };
    if( command_type < 2 ) {
        int idx = 0;
        for( idx = 0 ; idx < 3 ; idx++ ){
            if( !strncmp( wtypes[idx] , tokens[number_tokens-1] , 1 ) )
                wtype = idx;
        }
    }

    if( command_type == DEBUG ) {
        memset( input_buf , 0 , size+1 );
        pthread_mutex_lock(&lock);
        sprintf( input_buf , "echo mrd 0x%x 4 b | nc localhost 10878\r\n" , (u64_t*)u8_array );
        pthread_mutex_unlock(&lock);
        
        lwip_send(s, input_buf, strlen(input_buf), 0);
        
        pthread_mutex_lock(&lock);
        sprintf( input_buf , "echo mrd 0x%x 4 h | nc localhost 10878\r\n" , (u64_t*)u16_array );
        pthread_mutex_unlock(&lock);
        
        lwip_send(s, input_buf, strlen(input_buf), 0);
        
        pthread_mutex_lock(&lock);
        sprintf( input_buf , "echo mrd 0x%x 2 w | nc localhost 10878\r\n" , (u64_t*)u32_array );
        pthread_mutex_unlock(&lock);

        return lwip_send(s, input_buf, strlen(input_buf), 0);        
    }

    u16_t number_of_words = 1;
    if( command_type == MRD ) {
        if( number_tokens == 2 )
            number_of_words = 0;
        else if( number_tokens > 2 ) {
            if( wtype == N ) {
                number_of_words = strtoul( tokens[number_tokens-1] , pEnd , 0 );
            }
            else {
                number_of_words = strtoul( tokens[number_tokens-2] , pEnd , 0 );
            }
        }
    }
    else if( command_type == MWR ) {
        if( number_tokens == 3 )
            number_of_words = 1;
        else if( number_tokens > 3 ) {
            if( wtype == N ) {
                number_of_words = strtoul( tokens[number_tokens-1] , pEnd , 0 );
            }
            else {
                number_of_words = strtoul( tokens[number_tokens-2] , pEnd , 0 );
            }
        }
    }

    if( command_type == MRD && number_tokens == 2 )
        number_of_words = 1;

    u32_t address = 0;
    u32_t values[NTELNETTOKENS] = {0};

    if( command_type < 2 ) {
        if( number_tokens > 1 ) {
            address = strtoul( tokens[1] , pEnd , 0 );
        }
    }
    
    int idx = 0;

    if( command_type == MWR ) {
        for( idx = 0 ; idx < number_of_words ; idx++ ) {
            values[idx] = strtoul( tokens[idx+2] , pEnd , 0 );
            pthread_mutex_lock(&lock);
            if( wtype == N || wtype == W ) { /* WORD, u32_t */
                u32_t * tval = NULL;
                tval = ( (u32_t*)address + idx );
                *tval = (u32_t)values[idx];
            }
            else if( wtype == H ) { /* HALF, u16_t */
                u16_t * tval = NULL;
                tval = ( (u16_t*)address + idx );
                *tval = (u16_t)values[idx];
            }
            else if( wtype == B ) { /* BYTE, u8_t */
                u8_t * tval = NULL;
                tval = ( (u8_t*)address + idx );
                *tval = (u8_t)values[idx];
            }
            pthread_mutex_unlock(&lock);
        }
    }

//     printf( "address 0x%x\n" , address );
    
    if( command_type == MRD ) {
        for( idx = 0 ; idx < number_of_words ; idx++ ) {
            pthread_mutex_lock(&lock);
            if( wtype == N || wtype == W ) { /* WORD, u32_t */
                u32_t * tval = NULL;
                tval = ( (u32_t*)address + idx );
                values[idx] = *tval;
            }
            else if( wtype == H ) { /* HALF, u16_t */
                u16_t * tval = NULL;
                tval = ( (u16_t*)address + idx );
                values[idx] = *tval;
            }
            else if( wtype == B ) { /* BYTE, u8_t */
                u8_t * tval = NULL;
                tval = ( (u8_t*)address + idx );
                values[idx] = *tval;
            }
            pthread_mutex_unlock(&lock);
        }
    }

    memset( input_buf , 0 , RECV_BUF_SIZE );
    char tstr[RECV_BUF_SIZE];
    if( command_type == MRD ) {
        for( idx = 0 ; idx < number_of_words ; idx++ ) {
            sprintf( tstr , "%s 0x%x" , input_buf , values[idx] );
            sprintf( input_buf , "%s" , tstr );
        }
    }
    sprintf( tstr , "%s\r\n" , input_buf );
    sprintf( input_buf , "%s" , tstr );

    int ret_val = 0;
    if( strlen(input_buf)>2  ) {
        ret_val = lwip_send(s, input_buf, strlen(input_buf), 0);
    }
    memset( input_buf , 0 , RECV_BUF_SIZE );
    return ret_val;
}

void error(const char *msg)
{
    perror(msg);
    exit(1);
}

void telnet_readsocket( int sock , int sockfd ) {
    int n;
    char buffer[256];
    memset(buffer,0,256);
    n = read(sock,buffer,255);
    if (n < 0) error("ERROR reading from socket");    
    printf("Here is the message: %s\n",buffer);
    n = telnet_response(sock, buffer, strlen(buffer), sockfd );
    //      n = write(sock,"I got your message",18);
    if (n < 0) error("ERROR writing to socket");
}

void * server_thread(void * a)
{
     int portno = 10878;
     int sockfd, newsockfd;
     socklen_t clilen;
     struct sockaddr_in serv_addr, cli_addr;
     int n;
     sockfd = socket(AF_INET, SOCK_STREAM, 0);
     if (sockfd < 0) 
        error("ERROR opening socket");
//      bzero((char *) &serv_addr, sizeof(serv_addr));
     memset( (char*) &serv_addr , 0 , sizeof(serv_addr) );
     serv_addr.sin_family = AF_INET;
     serv_addr.sin_addr.s_addr = INADDR_ANY;
     serv_addr.sin_port = htons(portno);
     if (bind(sockfd, (struct sockaddr *) &serv_addr,
              sizeof(serv_addr)) < 0) 
              error("ERROR on binding");
     listen(sockfd,5);
     clilen = sizeof(cli_addr);
     while( ( newsockfd = accept(sockfd, 
                    (struct sockaddr *) &cli_addr, 
                    &clilen) ) > 0 ) {
        if (newsockfd < 0) 
            error("ERROR on accept");
        telnet_readsocket( newsockfd , sockfd );
        close(newsockfd);
     }
     close(sockfd);
     return 0;
}

int main()
{
    printf( "starting main\n" );
    
    pthread_t net_thread;
    pthread_mutex_init( &lock , NULL );
    
    if(pthread_create(&net_thread, NULL, server_thread, NULL)) {
      printf("\n ERROR creating thread");
      exit(1);
    }
    
    if(pthread_join(net_thread, NULL)){
        printf("\n ERROR joining thread");
        exit(1);
    }        

    
    pthread_mutex_destroy(&lock);
    
    return 0;
}
