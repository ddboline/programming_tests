/* * C++ Program to Implement Selection Sort */
#include <stdio.h>
// #include <conio.h>
#include <iostream>
#include <vector>
#include <cstdlib>
#include <ctime>
using namespace std;

int selection_sort_vector(const vector<int> & inpvec, vector<int> & outvec) {
    int lowindex, lowkey, temp, n = inpvec.size();

    if(inpvec.size() != outvec.size())
        return -1;
    for(int idx = 0; idx < n; idx++)
        outvec[idx] = inpvec[idx];

    for(int idx = 0; idx <= n-1; idx++) {
        lowindex = idx;
        lowkey = outvec[idx];
        for(int jdx = idx+1; jdx <= n; jdx++) {
            if(outvec[jdx] < lowkey) {
                lowkey = outvec[jdx];
                lowindex = jdx;
            }
        }
        temp = outvec[idx];
        outvec[idx] = outvec[lowindex];
        outvec[lowindex] = temp;
    }

    return 0;
}

// int selection_sort_array(int arrsize, int inparray[], int outarray[]){
//     cout << "size " << arrsize << " " << sizeof(inparray) << " " << sizeof(outarray) << endl;
// }

int main(int argc, char ** argv) {
    int seed = 8675309;
    if(argc>1){
        seed = atoi(argv[1]);
    }
    printf("seed %d\n" , seed);
    srand(seed);
    
    int vector_size = 10;
    vector<int> input_vector(vector_size), output_vector(vector_size);
    for(vector<int>::iterator it = input_vector.begin(); it != input_vector.end(); it++){
        *it = rand() % 100;
    }
    
    cout << "Input array             :";
    for(vector<int>::iterator it = input_vector.begin(); it != input_vector.end(); it++){
        cout << " " << *it;
    }
    cout << endl;
    
    int retval = selection_sort_vector(input_vector, output_vector);

    cout << "Selection Sorted array 1:";
    for(vector<int>::iterator it = output_vector.begin(); it != output_vector.end(); it++){
        cout << " " << *it;
    }
    cout << endl;
    
    int lowindex,lowkey,temp,n=vector_size;
    int a[n];

    for (int i = 0; i < n; i++) {
        a[i] = input_vector[i];
    }
    cout << "Selection Sorted array 1:";
    for (int k = 0; k < n; k++) {
        cout << " " << a[k];
    }
    cout << endl;
    
    for (int i = 0; i <= n - 1; i++) {
        lowindex = i;
        lowkey = a[i];
        for (int j = i + 1; j <= n; j++) {
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
    for (int k = 0; k < n; k++) {
        cout << " " << a[k];
    }
    cout << endl;
}
