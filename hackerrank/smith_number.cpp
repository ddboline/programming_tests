#include <cmath>
#include <cstdio>
#include <vector>
#include <iostream>
#include <algorithm>
using namespace std;

vector<int> prime_factors(int pval){
    int cval = pval;
    vector<int> factors;
    vector<int> p;
    int k=0, n=2;
    while(k < cval){
        int i = 0;
        while(i < k && n % p[i] != 0)
            i++;
        if(i == k){
            p.push_back(n);
            k++;
            while(cval % n == 0){
                factors.push_back(n);
                cval /= n;
            }
        }
        if( k > sqrt(cval) ){
            factors.push_back(cval);
            break;
        }
        n++;
    }
    return factors;
}

int sum_of_digits(int number){
    int sum_of_digit = 0;
    long int divisor = 1;
    while(divisor < number){
        sum_of_digit += (number/divisor) % 10;
        divisor *= 10;
    }
    return sum_of_digit;
}

int smith_number(int number){
    if(number == 1)
        return 0;
    int sum_of_prime_dig = 0;
    vector<int> primes = prime_factors(number);
    for(vector<int>::iterator it=primes.begin(); it!=primes.end(); it++){
        sum_of_prime_dig += sum_of_digits((*it));
    }
    return (sum_of_prime_dig == sum_of_digits(number));
}

int main(int argc, char ** argv){
    int val = atoi(argv[1]);
    cout << smith_number(val) << endl;
}
