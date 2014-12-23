#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>

int main( int argc , char ** argv ) {
    int x = 0;
    int y = 5;
    if( argc > 1 )
        x = atoi( argv[1] );
    if( argc > 2 )
        y = atoi( argv[2] );
    printf( "%d %d %d\n" , x , y , (x>5) ? x : y );
    return 0;
}