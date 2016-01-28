#include <iostream>
#include <string>
#include <future>
 
#define CYCLES 100

using namespace std;

void test(const string & name) {
    for (int i = 0; i < CYCLES; i++) {
            cout << "Hello world (" << name << ") " << (i + 1) << endl;
    }
}
 
int main () {
    string t1("GODZILLA");
    string t2("DRACULA");
    string t3("GRU");

    auto async_task1 = async(launch::async, test, t1);
    auto async_task2 = async(launch::async, test, t2);
    auto async_task3 = async(launch::async, test, t3);

    async_task1.get();
    async_task2.get();
    async_task3.get();

    return 0;
}
