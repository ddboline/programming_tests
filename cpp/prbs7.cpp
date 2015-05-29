#include <string>
#include <iostream>
#include <memory>
#include <vector>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

using namespace std;

int prbs7(uint8_t start, vector<uint8_t> & output){
    uint8_t a = start;
    for(int i=1;; i++) {
        int newbit = (((a >> 6) ^ (a >> 5)) & 1);
        a = ((a << 1) | newbit) & 0x7f;
        output.push_back(a);
        if (a == start) {
            return i;
        }
    }
    return 0;
}

unsigned char base64_char(uint8_t ch){
    uint8_t tmp;
    if(ch >= 0 && ch < 26)
        tmp = ch + 65;
    else if(ch >= 26 && ch < 52)
        tmp = ch + 97;
    else if(ch >= 52 && ch < 62)
        tmp = ch + 48;
    else if(ch == 62)
        tmp = 43;
    else if(ch == 63)
        tmp = 47;
    else
        tmp = 61;
    return tmp;
}

int base64_convert(const vector<uint8_t> & input, string & output){
    auto in_it = input.begin();
    while(true){
        int triplet = *in_it;
        ++in_it;
        if(in_it != input.end()) {
            triplet |= (*in_it) << 8;
            ++in_it;
            if(in_it != input.end()) {
                triplet |= (*in_it) << 8;
            }
            else
                break;
        }
        else
            break;
        cout << triplet << endl;
        char * tstr = (char*)malloc(5 * sizeof(char));
        
        for(int i = 0 ; i < 4 ; i++ ){
            uint8_t tmp = ((triplet >> (i*3)) & 0x3F);
            tstr[i] = base64_char(tmp) & 0x7F;
//             cout << i << " " << tmp << " " << tchar << endl;
        }
        tstr[4] = 0x0;
        printf("%s\n", tstr);
    }
}

int main(int argc, char** argv) {
    time_t timer;
    time(&timer);
    uint8_t start = timer & 0x7F;
    if(argc>1){
        start = atoi(argv[1]) & 0x7F;
        if(start == 0)
            start = 1432838330 & 0x7F;
    }
    uint8_t a = start;
    vector<uint8_t> output;
    int period = prbs7(start, output);
    for(auto a: output)
        printf("%02x", a);
    cout << endl;
    cout << "\nrepetition period is " << period << "\n";
    string result;
    base64_convert(output, result);
}
