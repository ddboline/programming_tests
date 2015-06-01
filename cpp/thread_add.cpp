#include <thread>
#include <mutex>
#include <atomic>
#include <vector>
#include <iostream>

using namespace std;

mutex mtx;

const int NITER = 100000;
int count;
int count1;
atomic<unsigned int> count2;

class local_lock {
    mutex & mtx_;
public:
    local_lock(mutex & mtx): mtx_(mtx){ mtx_.lock(); };
    ~local_lock() { mtx_.unlock(); }
};

int thread_add(int threadid)
{
  int i, tmp;
  for(i = 0; i < NITER; i++)
    {
      tmp = count;      /* copy the global count locally */
      tmp = tmp+1;      /* increment the local copy */
      count = tmp;      /* store the local value into the global count */
      ++count2;
      local_lock current_lock(mtx);
      ++count1;
    }
    return 0;
}

int main(int argc, char ** argv){
    count = 0;
    count1 = 0;
    count2 = 0;

    thread th1(thread_add, 0), th2(thread_add, 1);
    th1.join();
    th2.join();
    cout << "count " << count << " count1 " << count1 << " count2 " << count2 << endl;
    
    count = 0;
    count1 = 0;
    count2 = 0;
    
    vector<thread> threads;
    for(int idx=0; idx<10; idx++)
        threads.push_back(thread(thread_add, idx));
    for(auto & it: threads)
        it.join();

    cout << "count " << count << " count1 " << count1 << " count2 " << count2 << endl;

    return 0;
}
