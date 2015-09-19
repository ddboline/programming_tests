#include <iostream>
#include <future>
 
#define CYCLES 100
 
void test(const char* name) {
    int i;
    for (i = 0; i < CYCLES; i++) {
            std::cout << "Hello world (" << name << ") " << (i + 1) << std::endl;
    }
}
 
int main () {
    const char* t1 = "GODZILLA";
    const char* t2 = "DRACULA";
    const char* t3 = "GRU";

    auto async_task1 = std::async(std::launch::async, test, t1);
    auto async_task2 = std::async(std::launch::async, test, t2);
    auto async_task3 = std::async(std::launch::async, test, t3);

    async_task1.get();
    async_task2.get();
    async_task3.get();

    return 0;
}
