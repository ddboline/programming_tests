#include <iostream>
#include <string>
using namespace std;

int main() {
   // Complete the program
    string a, b;
    cin >> a >> b;
    cout << a.size() << " " << b.size() << endl;
    cout << a+b << endl;
    string ap = a, bp = b;
    ap[0] = b[0];
    bp[0] = a[0];
    cout << ap << " " << bp << endl;
    return 0;
}
