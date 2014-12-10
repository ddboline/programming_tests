#include <stdio.h>
#include <stdlib.h>

#define MAXIMUM_NUMBER 10000
    
int primes( int kmax ) {
    int n = 2 , k = 0 , i;
    int p[MAXIMUM_NUMBER] = {};
    int result = 0;
    if( kmax > MAXIMUM_NUMBER )
        kmax = MAXIMUM_NUMBER;
    while( k < kmax ) {
        i = 0;
        while( i < k && n % p[i] != 0 )
            i++;
        if( i == k ) {
            p[k] = n;
            k++;
            result = n;
        }
        n++;
    }
    return result;
}

int main(int argc, char **argv)
{
    int maxprime = primes( 10000 );
    printf( "%d\n" , maxprime );
    return 0;
}

