#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <stdint.h>

int64_t atoi_impl( const char * inpstr ){
    int64_t outp = 0 , power = 1;
    int idx = 0, ascii_code;
    int inpstr_len = strlen( inpstr );
    char ascii_offset = '0';
    char current_char = *inpstr;
    for( idx = inpstr_len-1 ; idx >= 0 ; idx-- ){
        ascii_code = inpstr[idx];
        if(ascii_code == '+')
            return outp;
        else if(ascii_code == '-'){
            outp *= -1;
            return outp;
        }
        else if(ascii_code >= ascii_offset && ascii_code <= ascii_offset+9){
            outp += (ascii_code-ascii_offset)*power;
            power *= 10;
        }
    }
    return outp;
}

int main( int argc , char ** argv ) {
    int idx = 0;
    for( idx = 1 ; idx < argc ; idx++ ) {
        printf( "%s\n" , argv[idx] );
        printf( "%ld\n" , atol( argv[idx] ) );
        printf( "%ld\n" , atoi_impl( argv[idx] ) );
    }
    return 0;
}