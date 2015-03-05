#include <stdlib.h>
#include <stdio.h>
#include <math.h>

void is_possible(int r2, int k){
    int count = 0, a, b, a2, b2;
    int r = sqrt(r2);
    if(r2 - r == 0)
        count += 4;
    for(a=1; a<r; a++){
        a2 = a*a;
        for(b=1; b<a; b++){
            b2 = b*b;
            if((r2 - a2 - b2) == 0)
                count += 8;
        }
    }
    if(k<count)
        printf("impossible\n");
    else
        printf("possible\n");
}

int main(int argc, char ** argv){
    is_possible(1, 3);
    is_possible(1, 4);
    is_possible(4, 4);
    is_possible(25, 11);
    is_possible(25, 12);
}