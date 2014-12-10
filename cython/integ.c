#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <stdbool.h>
#include <complex.h>
#include <stdint.h>

// typedef unsigned char uint8_t;
// typedef unsigned short uint16_t;
// typedef unsigned int uint32_t;
// typedef unsigned long int uint64_t;

long double f( long double x ) {
    return x*x - x;
}

long double integrate_f( long double a , long double b , long int N ) {
    long int i = 0;
    long double s = 0, dx;
    dx = ( b - a ) / N;
    while( i < N ) {
        s += f( a + i * dx );
        i++;
    }
    return s * dx;
}

int main( int argc , char ** argv ) {
    long double retval = integrate_f( 0 , 1 , 5e7 );
    // printf( "%ld %ld %ld %ld %ld %ld %ld %ld %ld %ld\n" , sizeof(long double)*8 , sizeof(double)*8 , sizeof(long int)*8 , sizeof(int)*8 , sizeof(uint64_t)*8 , sizeof(uint32_t)*8 , sizeof(uint16_t)*8 , sizeof(uint8_t)*8 , sizeof(bool) , sizeof(double complex) ) ;
    printf( "%.12Lf\n" , retval );
    return 0;
}