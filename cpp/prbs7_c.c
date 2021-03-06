#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>

void prb7(uint8_t start){
    uint8_t a = start;
    int i = 1;
    for(i = 1;; i++) {
        uint8_t newbit = (((a >> 6) ^ (a >> 5)) & 1);
        a = ((a << 1) | newbit) & 0x7f;
        printf("%x", a);
        if (a == start) {
            printf("\nrepetition period is %d\n", i);
            return ;
        }
    }
}

int main(int argc, char** argv) {
    uint8_t start = 0x02;
    if(argc>1){
        start = atoi(argv[1]) & 0x7F;
        printf("%s %x\n", argv[1], start);
    }
    prb7(start);
    return 0;
}
