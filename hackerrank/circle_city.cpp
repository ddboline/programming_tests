#include <cstdlib>
#include <cstdio>
#include <cmath>
#include <iostream>

using std::cout;
using std::cin;
using std::endl;

void is_possible(long r2, long k){
    long count = 0, a, b, a2, b2;
    long r = sqrt(r2);
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
    int t;
    long r2, k;
    cin >> t;
    for(int idx=0; idx<t; idx++){
        cin >> r2 >> k;
        is_possible(r2, k);
    }
}
