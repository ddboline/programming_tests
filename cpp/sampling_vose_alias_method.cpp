#include <vector>
#include <deque>
#include <random>
#include <iostream>
#include <time.h>
#include <chrono>
#include <functional>

using std::vector;
using std::deque;
using std::cout;
using std::endl;
using std::uniform_real_distribution;
using std::uniform_int_distribution;
using std::function;
using std::default_random_engine;
using std::chrono::system_clock;

class VoseAliasMethod{
    public:
        int prob_length;
        vector<double> alias_arr, prob_arr;
        function<int()> int_distribution;
        function<double()> real_distribution;

        VoseAliasMethod(const vector<double> & p, const default_random_engine & generator){
            prob_length = p.size();
            int_distribution = bind(uniform_int_distribution<int>(0, prob_length-1), generator);
            real_distribution = bind(uniform_real_distribution<double>(0.0, 1.0), generator);
            alias_arr.resize(prob_length);
            prob_arr.resize(prob_length);
            deque<int> small, large;
            auto scaled_p = p;
            for(auto & it : scaled_p)
                it *= prob_length;
            for(size_t idx=0; idx<scaled_p.size(); idx++){
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
            auto i = int_distribution();
            auto r = real_distribution();
            if(r<prob_arr[i])
                return i;
            else
                return alias_arr[i];
        }
};

int main(int argc, char ** argv){
    auto number = 6;
    vector<double> prob_array(number);
    auto seed = system_clock::now().time_since_epoch().count();
    default_random_engine generator(seed);
    function<double()> real_distribution = bind(uniform_real_distribution<double>(0.0,1.0), generator);
    for(auto & it : prob_array)
        it = real_distribution();
    auto sum = 0.0;
    for(auto it : prob_array)
        sum += it;
    for(auto & it : prob_array)
        it /= sum;
    for(auto it : prob_array)
        cout << it << " ";
    cout << endl;
    
    VoseAliasMethod v(prob_array, generator);
    vector<int> runs{10, 10, 10,
                     100, 100, 100, 
                     1000, 1000, 1000,
                     10000, 10000, 10000, 
                     100000, 100000, 100000, 
                     1000000, 1000000, 1000000, 
                     10000000, 10000000, 10000000,};
    auto t = clock();
    for(size_t idx=0; idx<runs.size(); idx++){
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
