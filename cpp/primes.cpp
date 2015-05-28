#include <vector>
#include <sstream>
#include <iostream>
#include <stdlib.h>

using namespace std;

int primes( const int pmax ) {
    int n = 3 , k = 0 , i;
    vector<int> p;
    p.push_back(2);
    int result = 0;
    while( n < pmax ) {
        i = 0;
        while( i < k && n % p[i] != 0 )
            i++;
        if( i == k ) {
            p.push_back(n);
            k++;
            result = n;
        }
        n++;
    }
    for(auto it: p)
        cout << it << " ";
    cout << endl;
    return p.size();
}

int main(int argc, char **argv)
{
    cout << argc << endl;
    if(argc > 1)
        cout << primes(atoi(argv[1])) << endl;
    return 0;
}
