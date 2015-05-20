#include <thread>
#include <mutex>
#include <atomic>

#include <iostream>
#include <vector>
#include <string>
#include <cstdlib>

using namespace std;

mutex mtx;

atomic<bool> ready(false);

void print_hello(int threadid){
    while(!ready)
        this_thread::yield();
    for(int idx=0; idx<10; idx++){
        mtx.lock();
        cout << "Hello there from thread " << threadid << " " << idx << endl;
        mtx.unlock();
        this_thread::yield();
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