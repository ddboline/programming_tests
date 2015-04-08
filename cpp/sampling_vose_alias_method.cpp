#include <vector>
#include <deque>
#include <random>
#include <iostream>

using namespace std;

class VoseAliasMethod{
    public:
        int prob_length;
        vector<double> alias_arr;
        vector<double> prob_arr;
        default_random_engine generator;

        VoseAliasMethod(vector<double> & p){
            prob_length = p.size();
            alias_arr.resize(prob_length);
            prob_arr.resize(prob_length);
            deque<int> small, large;
            vector<double> scaled_p(prob_length);
            for(int i=0; i<p.size(); i++){
                scaled_p[i] = p[i]*prob_length;
            }
            for(int idx=0; idx<scaled_p.size(); idx++){
                if(scaled_p[idx]<1)
                    small.push_back(idx);
                else
                    large.push_back(idx);
            }
            while(small.size()>0 && large.size()>0){
                int l = small[0];
                small.pop_front();
                int g = large[0];
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
                int g = large[0];
                large.pop_front();
                prob_arr[g] = 1;
            }
            while(small.size()>0){
                int l = small[0];
                small.pop_front();
                prob_arr[l] = 1;
            }
        };
        
        int generate(){
            uniform_int_distribution<int> int_distribution(0, prob_length-1);
            uniform_real_distribution<double> real_distribution(0.0,1.0);
            int i = int_distribution(generator);
            double r = real_distribution(generator);
            if(r<prob_arr[i])
                return i;
            else
                return alias_arr[i];
        }
};

int main(int argc, char ** argv){
    int number = 6;
    vector<double> prob_array(number);
    default_random_engine generator;
    uniform_real_distribution<double> real_distribution(0.0,1.0);
    for(int idx=0; idx<number; idx++){
        prob_array[idx] = real_distribution(generator);
    }
    double sum = 0;
    for(int idx=0; idx<number; idx++)
        sum += prob_array[idx];
    for(int idx=0; idx<number; idx++)
        prob_array[idx] /= sum;
    
    for(int idx=0; idx<number; idx++)
        cout << prob_array[idx] << " ";
    cout << endl;
    
    VoseAliasMethod v(prob_array);
    int runs[7] = {10, 100, 1000, 10000, 100000, 1000000, 10000000};
    for(int idx=0; idx<7; idx++){
        vector<double> hist(number);
        for(int jdx=0; jdx<runs[idx]; jdx++){
            int r = v.generate();
            hist[r] += 1;
        }
        sum = 0;
        for(int jdx=0; jdx<number; jdx++)
            sum += hist[jdx];
        for(int jdx=0; jdx<number; jdx++)
            hist[jdx] /= sum;
        cout << "run" << idx << " ";
        for(int jdx=0; jdx<number; jdx++)
            cout << hist[jdx] << " ";
        cout << endl;
    }
}
