#include <fstream>
#include <iostream>
#include <vector>
#include <string>

using namespace std;

vector<string> split(const string & input, string delim=","){
    vector<string> output;
    int begin_pos = 0;
    while(true){
        int new_pos = input.find(delim, begin_pos);
        int end_pos = new_pos;
        if(new_pos == -1)
            end_pos = input.size();
        auto sstr = input.substr(begin_pos, end_pos);
        output.push_back(sstr);
        begin_pos = end_pos + 1;
        if(new_pos == -1)
            break;
    }
    return output;
}

int main(){
    string st;
    ifstream f("islands.csv");
    while(getline(f, st)){
        auto output = split(st, string(1, 0x2c));
        for(auto s : output)
            cout << s << " ";
        cout << endl;
    }
};
