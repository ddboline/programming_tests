#include <fstream>
#include <iostream>
#include <vector>
#include <string>
#include <string.h>

using namespace std;

void removeChar(string & source, unsigned int index) {
    for(unsigned int i=0; i<source.size(); i++){
        if(i >= index){
            source[i] = source[i+1];
        }
    }
}

int main(int argc, char ** argv){
    if(argc > 1){
//         char * a = argv[1];
        string a(argv[1]);
        removeChar(a, 2);
        cout << a << " " << endl;
    }
};
