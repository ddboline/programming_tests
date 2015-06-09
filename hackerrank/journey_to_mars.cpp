#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;

long int integer_power(long int N, long int M) {
    long int result = 1;
    if(M>100)
        return pow(N, M);
    for(long int i=0; i<M; i++)
        result *= N;
    return result;
}

long int last_k_digits(long int N, long int TENK) {
    long int result = 1;
    if(N == 1)
        return result;
    else if (N % 2 == 0) {
        result *= last_k_digits(N/2, TENK);
        result %= TENK;
        result *= last_k_digits(N/2, TENK);
        result %= TENK;
    }
    else {
        long int result = 1;
        result *= last_k_digits((N-1)/2, TENK);
        result %= TENK;
        result *= last_k_digits((N-1)/2, TENK);
        result %= TENK;
        result *= 2;
        result %= TENK;
    }
    return result;
}

int main(int argc, char ** argv){
    int T;
    cin >> T;
    for(int i=0; i<T; i++){
        long int N, K;
        cin >> N >> K;
        int mval = K * log(10)/log(2);
        long int tenk = integer_power(10, K);
        long int lowest_k = last_k_digits(N-1, tenk);
        long double n1log102 = (N-1) * log(2)/log(10);
        long double power = n1log102 - int(n1log102) + K - 1;
        long int highest_k = pow(10, power);
        cout << (highest_k+lowest_k) << endl;
    }
}
