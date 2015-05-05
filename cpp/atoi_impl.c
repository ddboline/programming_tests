#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>

int64_t atoi_impl( const char * inpstr ){
    int64_t outp = 0 ;
    int idx, ascii_code;
    int64_t power = 1;
    int inpstr_len = strlen( inpstr );
    char ascii_offset = '0';
    // printf( "length %d\n" , inpstr_len );
    for( idx = inpstr_len-1 ; idx >= 0 ; idx-- ){
        ascii_code = inpstr[idx];
        if( ascii_code < ascii_offset || ascii_code > ascii_offset+9 ) {
            if( ascii_code == '+' ) continue;
            else if( ascii_code == '-' ) outp *= -1;
            else return outp;
            continue;
        }
        outp += ( ascii_code - ascii_offset ) * power;
        power *= 10;
        // printf( "%d 0x%x %lld\n" , idx , inpstr[idx] , outp );
    }
    return outp;
}

int main( int argc , char ** argv ) {
    int idx = 0;
    for( idx = 1 ; idx < argc ; idx++ ) {
        printf( "%s\n" , argv[idx] );
        printf( "%ld\n" , atoi_impl( argv[idx] ) );
    }
    return 0;
}