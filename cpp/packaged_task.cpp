// packaged_task example
#include <iostream>     // std::cout
#include <future>       // std::packaged_task, std::future
#include <chrono>       // std::chrono::seconds
#include <thread>       // std::thread, std::this_thread::sleep_for

using namespace std;

// count down taking a second for each value:
int countdown (int from, int to) {
  for (int i=from; i!=to; --i) {
    cout << i << '\n';
    this_thread::sleep_for(chrono::seconds(1));
  }
  cout << "Lift off!\n";
  return from-to;
}

int main(){
  packaged_task<int(int,int)> tsk (countdown);   // set up packaged_task
  future<int> ret = tsk.get_future();            // get future

  thread th (move(tsk),10,0);   // spawn thread to count down from 10 to 0

  // ...
  
  cout << " WHAT UP? " << endl;

  int value = ret.get();                  // wait for the task to finish and get result

  cout << "The countdown lasted for " << value << " seconds.\n";

  th.join();

  return 0;
}
