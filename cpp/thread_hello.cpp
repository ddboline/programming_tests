#include <thread>
#include <mutex>
#include <atomic>

#include <iostream>
#include <sstream>
#include <vector>
#include <string>
#include <cstdlib>

using namespace std;

mutex mtx;

atomic<bool> ready(false);

class local_lock {
    mutex & mtx_;
public:
    local_lock(mutex & mtx): mtx_(mtx){ mtx_.lock(); };
    ~local_lock() { mtx_.unlock(); }
};

void print_hello(int threadid){
    while(!ready)
        this_thread::yield();
    for(int idx=0; idx<10; idx++){
        local_lock current_lock(mtx);
        stringstream output;
        output << "Hello there from thread " << threadid << " " << idx << endl;
        cout << output.str();
    }
}

int main(int argc, char ** argv){
    vector<thread> threads;
    for(int idx=0; idx<10; idx++)
        threads.push_back(thread(print_hello, idx));
    ready = true;
    
    for(auto & it : threads) {
        it.join();
    }
}