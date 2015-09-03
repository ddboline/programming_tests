#include <fstream>
#include <iostream>
#include <vector>
#include <string>
#include <string.h>

using namespace std;

void removeChar(char * source, int index){
        // creates another char* with the same pointer as source
        char* scopy = &source[0];
        int len = strlen(source);
 
        // loops through the string, keeping its contents until index is found.
        for (int i =0; i< len; i++) {
 
                // checks if the current char doesnt match index char, current char to string
                if (i != index) {
                        *scopy = source[i];
                        scopy++;
                }   
        }
        // end new string
        *scopy = '\0';
}

int main(int argc, char ** argv){
    if(argc > 1){
        char * a = argv[1];
        removeChar(a, 2);
        cout << a << " " << endl;
    }
};
