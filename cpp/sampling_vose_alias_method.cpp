#include <vector>
#include <deque>
#include <random>
#include <iostream>
#include <time.h>
#include <chrono>

using namespace std;

class VoseAliasMethod{
    public:
        int prob_length;
        vector<double> alias_arr, prob_arr;
        default_random_engine generator;
        uniform_int_distribution<int> int_distribution;
        uniform_real_distribution<double> real_distribution;

        VoseAliasMethod(vector<double> & p){
            prob_length = p.size();
            int_distribution = uniform_int_distribution<int>(0, prob_length-1);
            real_distribution = uniform_real_distribution<double>(0.0, 1.0);
            alias_arr.resize(prob_length);
            prob_arr.resize(prob_length);
            deque<int> small, large;
            auto scaled_p = p;
            for(auto & it : scaled_p)
                it *= prob_length;
            for(auto idx=0; idx<scaled_p.size(); idx++){
                if(scaled_p[idx]<1)
                    small.push_back(idx);
                else
                    large.push_back(idx);
            }
            while(small.size()>0 && large.size()>0){
                auto l = small.front();
                small.pop_front();
                auto g = large.front();
                large.pop_front();
                prob_arr[l] = scaled_p[l];
                alias_arr[l] = g;
                scaled_p[g] = (scaled_p[g]+scaled_p[l])-1;
                if(scaled_p[g]<1)
                    small.push_back(g);
                else
                    large.push_back(g);
            }
            while(large.size()>0){
                auto g = large.front();
                large.pop_front();
                prob_arr[g] = 1;
            }
            while(small.size()>0){
                auto l = small.front();
                small.pop_front();
                prob_arr[l] = 1;
            }
        };
        
        int generate(){
            auto i = int_distribution(generator);
            auto r = real_distribution(generator);
            if(r<prob_arr[i])
                return i;
            else
                return alias_arr[i];
        }
};

int main(int argc, char ** argv){
    auto number = 6;
    vector<double> prob_array(number);
    auto seed = chrono::system_clock::now().time_since_epoch().count();
    default_random_engine generator(seed);
    uniform_real_distribution<double> real_distribution(0.0,1.0);
    for(auto & it : prob_array)
        it = real_distribution(generator);
    auto sum = 0.0;
    for(auto it : prob_array)
        sum += it;
    for(auto & it : prob_array)
        it /= sum;
    for(auto it : prob_array)
        cout << it << " ";
    cout << endl;
    
    VoseAliasMethod v(prob_array);
    vector<int> runs{10, 10, 10,
                     100, 100, 100, 
                     1000, 1000, 1000,
                     10000, 10000, 10000, 
                     100000, 100000, 100000, 
                     1000000, 1000000, 1000000, 
                     10000000, 10000000, 10000000,};
    auto t = clock();
    for(auto idx=0; idx<runs.size(); idx++){
        vector<double> hist(number);
        for(auto jdx=0; jdx<runs[idx]; jdx++)
            hist[v.generate()] += 1;
        sum = 0;
        for(auto jdx=0; jdx<number; jdx++)
            sum += hist[jdx];
        for(auto jdx=0; jdx<number; jdx++)
            hist[jdx] /= sum;
        t = clock() - t;
        cout << "run" << idx << " " << runs[idx] << " " << t/1e6 << " ";
        for(auto jdx=0; jdx<number; jdx++)
            cout << hist[jdx] << " ";
        cout << endl;
    }
}
