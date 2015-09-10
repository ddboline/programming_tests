#include <iostream>
#include <sstream>
#include <cstdio>
#include <vector>
#include <string>
#include <boost/algorithm/string.hpp>

using namespace std;

vector<int> string_to_numbers(const vector<string> & output){
    vector<int> numbers;
    for(auto it=output.begin(); it!=output.end(); ++it){
        try {
            numbers.push_back(stoi(*it));
        }
        catch(invalid_argument){
            continue;
        }
    }
    return numbers;
}

int split_string_manual(const string & input, vector<string> & output, const string & delim){
    string current = "";
    for(auto it=input.begin(); it!=input.end(); ++it){
        auto chr = (*it);
        if(chr == delim[0]){
            output.push_back(current);
            current = "";
        }
        else
            current += chr;
    }
    output.push_back(current);
    return 0;
}

int split_string_boost(const string & input, vector<string> & output, const string & delim){
    boost::algorithm::split(output, input, boost::is_any_of(","));
    return 0;
}

void print_strings(vector<string> & input){
    vector<int> numbers = string_to_numbers(input);
    for(auto it=numbers.begin(); it!=numbers.end(); ++it)
        cout << (*it) << " ";
    cout << endl;
}

int main(int argc, char ** argv){
    string delim = ",";
    string input = "0,1234,5,1234";
    vector<string> output;
    split_string_manual(input, output, delim);
    print_strings(output);
    output.resize(0);
    split_string_boost(input, output, delim);
    print_strings(output);

    for(int i=1; i<argc; i++){
        string input(argv[i]);
        output.resize(0);
        split_string_manual(input, output, delim);
        print_strings(output);
    }
    
    return 0;
}
