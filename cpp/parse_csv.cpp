#include <fstream>
#include <iostream>
#include <vector>
#include <string>

using namespace std;

int split(string & input, vector<string> & output, string delim=","){
    int begin_pos = 0;
    while(true){
        int new_pos = input.find(delim, begin_pos);
//         cout << input << " new_pos " << new_pos << " " << delim << " " << begin_pos << endl;
        int end_pos = new_pos;
        if(new_pos == -1)
            end_pos = input.size();
        auto sstr = input.substr(begin_pos, end_pos);
//         printf("begin_pos %lu end_pos %lu sstr %s\n", begin_pos, end_pos, sstr.data());
        output.push_back(sstr);
        begin_pos = end_pos + 1;
        if(new_pos == -1)
            break;
    }
    return 0;
}

int main(){
    string st;
    vector<string> output;
    ifstream f("islands.csv");
    while(getline(f, st)){
        split(st, output, string(1, 0x2c));
        for(auto s : output)
            cout << s << " ";
        cout << endl;
        output.resize(0);
    }
};