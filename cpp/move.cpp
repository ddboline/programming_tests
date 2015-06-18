#include <iostream>
#include <utility>
#include <vector>
#include <string>

#include <list>
#include <iterator>
#include <thread>
#include <chrono>

using std::cout;
using std::endl;
using std::vector;
using std::string;
using std::thread;
using std::back_inserter;
using std::list;
using std::chrono::seconds;
using std::this_thread::sleep_for;

void f(int n) {
    sleep_for(seconds(n));
    cout << "thread " << n << " ended" << '\n';
}
 
int main() {
    string str = "Hello";
    vector<string> v;
 
    // uses the push_back(const T&) overload, which means 
    // we'll incur the cost of copying str
    v.push_back(str);
    cout << "After copy, str is \"" << str << "\"\n";
 
    // uses the rvalue reference push_back(T&&) overload, 
    // which means no strings will be copied; instead, the contents
    // of str will be moved into the vector.  This is less
    // expensive, but also means str might now be empty.
    v.push_back(move(str));
    cout << "After move, str is \"" << str << "\"\n";
 
    cout << "The contents of the vector are \"" << v[0]
                                         << "\", \"" << v[1] << "\"\n";
 
    // string move assignment operator is often implemented as swap,
    // in this case, the moved-from object is NOT empty
    string str2 = "Good-bye";
    cout << "Before move from str2, str2 = '" << str2 << "'\n";
    v[0] = move(str2);
    cout << "After move from str2, str2 = '" << str2 << "'\n";

    
    vector<thread> v_t;
    v_t.emplace_back(f, 1);
    v_t.emplace_back(f, 2);
    v_t.emplace_back(f, 3);
    list<thread> l;
    // copy() would not compile, because thread is noncopyable
 
    move(v_t.begin(), v_t.end(), back_inserter(l)); 
    for (auto& t : l) t.join();
    return 0;
}
