/* * C++ Program to Implement Selection Sort */
#include <stdio.h>
// #include <conio.h>
#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
using namespace std;

vector<int> selection_sort_vector(const vector<int> & inpvec) {
    int lowindex=0, lowkey=0, temp=0, n = inpvec.size();
    vector<int> outvec(n);

    for(int idx = 0; idx < n; idx++)
        outvec[idx] = inpvec[idx];

    for(int idx = 0; idx < n; idx++) {
        lowindex = idx;
        lowkey = outvec[idx];
        for(int jdx = idx+1; jdx < n; jdx++) {
            if(outvec[jdx] < lowkey) {
                lowkey = outvec[jdx];
                lowindex = jdx;
            }
        }
        temp = outvec[idx];
        outvec[idx] = outvec[lowindex];
        outvec[lowindex] = temp;
    }

    return outvec;
}

void print_array(int size, int arr[]){
    for(int i=0; i<size; i++){
        cout << " " << arr[i];
    }
    cout << endl;
}

void print_vector(const vector<int> & vec){
    for(auto & it: vec)
        cout << " " << it;
    cout << endl;
}

int main(int argc, char ** argv) {
    int seed = 8675309;
    if(argc>1){
        seed = atoi(argv[1]);
    }
    printf("seed %d\n" , seed);
    srand(seed);
    
    int vector_size = 10;
    vector<int> input_vector(vector_size);
    for(auto & it: input_vector)
        it = rand() % 100;
    
    cout << "Input array             :";
    print_vector(input_vector);

    auto output_vector = selection_sort_vector(input_vector);

    cout << "Selection Sorted array 1:";
    print_vector(output_vector);

    int lowindex=0, lowkey=0, temp=0, n=vector_size;
    int a[n];

    for (int i = 0; i < n; i++) {
        a[i] = input_vector[i];
    }

    for (int i = 0; i < n; i++) {
        lowindex = i;
        lowkey = a[i];
        for (int j = i + 1; j < n; j++) {
            if (a[j] < lowkey) {
                lowkey = a[j];
                lowindex = j;
            }
        }
        temp = a[i];
        a[i] = a[lowindex];
        a[lowindex] = temp;
    }
    cout << "Selection Sorted array 2:";
    print_array(n, a);
}
