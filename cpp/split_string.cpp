#include <iostream>
#include <sstream>
#include <cstdio>
#include <vector>
#include <string>
#include <boost/algorithm/string.hpp>

using namespace std;

vector<int> string_to_numbers(const vector<string> & output){
    vector<int> numbers;
    for(auto it=output.begin(); it!=output.end(); ++it)
        numbers.push_back(stoi(*it));
    return numbers;
}

int split_string_manual(const string & input, const string & delim){
    vector<string> output;
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
    vector<int> numbers = string_to_numbers(output);
    for(auto it=numbers.begin(); it!=numbers.end(); ++it)
        cout << (*it) << " ";
    cout << endl;
    return 0;
}

int split_string_boost(const string & input, const string & delim){
    vector<string> output;
    boost::algorithm::split(output, input, boost::is_any_of(","));
    vector<int> numbers = string_to_numbers(output);
    for(auto it=numbers.begin(); it!=numbers.end(); ++it)
        cout << (*it) << " ";
    cout << endl;
    return 0;
}

int main(int argc, char ** argv){
    string delim = ",";
    string input = "0,1234,5,1234";
    split_string_manual(input, delim);
    split_string_boost(input, delim);
    return 0;
}
