#include <string>
#include <iostream>
#include <sstream>
#include <memory>
#include <vector>
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <boost/archive/iterators/base64_from_binary.hpp>
#include <boost/archive/iterators/insert_linebreaks.hpp>
#include <boost/archive/iterators/transform_width.hpp>
#include <boost/archive/iterators/ostream_iterator.hpp>

using namespace std;
using namespace boost::archive::iterators;

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
    unique_ptr<char> b(new char(output.size()));
    stringstream os;
    for(auto a: output) {
        printf("%02x", a);
        char b = a;
        os << b;
    }
    cout << endl;
    cout << "\nrepetition period is " << period << "\n";
    
    string s = os.str();
    stringstream ss;
    typedef insert_linebreaks<base64_from_binary<transform_width<const char *, 6, 8> >, 4096> base64_enc;
    
    std::copy(base64_enc(s.c_str()), base64_enc(s.c_str() + s.size()), std::ostream_iterator<char>(ss));
    
    cout << ss.str() << endl;
}
