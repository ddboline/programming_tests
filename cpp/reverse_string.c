#include <stdlib.h>
#include <stdio.h>
#include <string.h>

char * reverse_string( const char * inp_str ){
    int inp_str_len = strlen( inp_str );
    char * newstr = malloc( (inp_str_len+1)*sizeof(char) );
    int idx = 0;
    for( idx = 0 ; idx < inp_str_len ; idx++ ) {
        newstr[idx] = inp_str[inp_str_len-1-idx];
    }
    return newstr;
}

int reverse_string_inplace(char * inp_str){
    int inp_str_len = strlen(inp_str);
    int idx = 0;
    char temp;
    for(idx=0; idx < inp_str_len/2; idx++){
        temp = inp_str[idx];
        inp_str[idx] = inp_str[inp_str_len-idx-1];
        inp_str[inp_str_len-idx-1] = temp;
    }
    return 0;
}

int main(int argc, char ** argv){
    /* Silly little program to reverse a string*/
    char * rev_string = NULL;
    int idx = 0;
    for( idx = 1 ; idx < argc ; idx++ ){
        printf( "%s " , argv[idx] );
    }
    printf( "\n" );
    for( idx = (argc-1) ; idx >= 1 ; idx-- ) {
        rev_string = reverse_string( argv[idx] );
        printf( "%s " , rev_string );
    }
    printf( "\n" );
    for( idx = (argc-1) ; idx >= 1 ; idx-- ) {
        strcpy(rev_string, argv[idx]);
        reverse_string_inplace(rev_string);
        printf( "%s " , rev_string );
    }
    printf( "\n" );
    if(rev_string)
        free(rev_string);
    return 0;
}
