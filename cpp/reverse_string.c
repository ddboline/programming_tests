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
        free(rev_string);
    }
    printf( "\n" );
    
    // char * teststr = "I'm feeling lucky!";
    // int teststr_len = strlen( teststr );
    // char * newstr = malloc( teststr_len+1 );
    // memset( newstr , 0 , teststr_len+1 );
    // int idx = 0;
    // for( idx=0 ; idx < strlen(teststr) ; idx++ ) {
    //     newstr[idx] = teststr[teststr_len-idx-1];
    //     printf( "%d %d %c %c\n" , idx , teststr_len-idx-1 , newstr[idx] , teststr[teststr_len-idx-1] );
    // }
    // printf( "%s\n" , newstr );
}