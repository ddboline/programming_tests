#include <random>
#include <iostream>
#include <memory>
#include <functional>

using namespace std;

void f(int n1, int n2, int n3, const int& n4, int n5)
{
    cout << n1 << ' ' << n2 << ' ' << n3 << ' ' << n4 << ' ' << n5 << '\n';
}
 
int g(int n1)
{
    return n1;
}
 
struct Foo {
    void print_sum(int n1, int n2)
    {
        cout << n1+n2 << '\n';
    }
    int data = 10;
};
 
int main()
{
    using namespace placeholders;  // for _1, _2, _3...
 
    // demonstrates argument reordering and pass-by-reference
    int n = 7;
    // (_1 and _2 are from placeholders, and represent future
    // arguments that will be passed to f1)
    auto f1 = bind(f, _2, _1, 42, cref(n), n);

    f1(1, 2, 1001); // 1 is bound by _2, 2 is bound by _1, 1001 is unused
 
    // nested bind subexpressions share the placeholders
    auto f2 = bind(f, _3, bind(g, _3), _3, 4, 5);
    f2(10, 11, 12);
 
    // common use case: binding a RNG with a distribution
    default_random_engine e;
    uniform_int_distribution<> d(0, 10);
    function<int()> rnd = bind(d, e); // a copy of e is stored in rnd
    for(int n=0; n<10; ++n)
        cout << rnd() << ' ';
    cout << '\n';
 
    // bind to a member function
    Foo foo;
    auto f3 = bind(&Foo::print_sum, &foo, 95, _1);
    f3(5);
 
    // bind to member data
    auto f4 = bind(&Foo::data, _1);
    cout << f4(foo) << '\n';
 
    // smart pointers can be used to call members of the referenced objects, too
    cout << f4(make_shared<Foo>(foo)) << '\n'
              << f4(unique_ptr<Foo>(new Foo(foo))) << '\n';
}
