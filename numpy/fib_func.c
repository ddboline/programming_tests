#include <stdlib.h>
#include <stdio.h>

int fib_func( int n ) {
    if( n == 0 )
        return 1;
    else if( n == 1 )
        return 1;
    else if( n >= 2 )
        return fib_func( n - 1 ) + fib_func( n - 2 );
    else
        exit(0);
}

int main( int argc , char ** argv ) {
    int i = 0;
    for( i = 0 ; i < 20 ; i++ ) {
        printf( "%d %d\n" , i , fib_func( i ) );
    }
    return 0;
}
