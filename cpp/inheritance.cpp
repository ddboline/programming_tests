#include <iostream>
#include <sstream>
#include <string>

using namespace std;

class test_class {
public:
    double member_a_ = 0.01;
    int member_b_ = 3;
    test_class() {};
    ~test_class() {};
    string member_c() { return member_c_; };
    void set_member_c(string s) { member_c_ = s; };
private:
    string member_c_ = "YO";
protected:
    unsigned int member_d_ = 5;
};

class test_class_2 : public test_class {
public:
    test_class_2(test_class & test) : test_class(test) {};
    ~test_class_2() {};
    double member_e_ = 1.234;
};

int main(int argc, char ** argv){
    stringstream os;
    for(auto i=0; i<26; i++)
        os << static_cast<char>(0x41+i);
    os << static_cast<char>(0x20);
    for(auto i=0; i<26; i++)
        os << static_cast<char>(0x61+i);
    cout << os.str() << endl;
    
    test_class cobj;
    cout << cobj.member_a_ << " " << cobj.member_b_ << " " << cobj.member_c() << endl;
    cobj.member_a_ = 1.234;
    cobj.member_b_ = 15;
    cobj.set_member_c("WHAT UP?");
    cout << cobj.member_a_ << " " << cobj.member_b_ << " " << cobj.member_c() << endl;
    
    test_class_2 cobj2(cobj);
    cout << cobj2.member_a_ << " " << cobj2.member_b_ << " " << cobj.member_c() << endl;
    cobj2.member_a_ = 2.4879;
    cobj2.member_b_ = 75;
    cout << cobj2.member_a_ << " " << cobj2.member_b_ << " " << cobj.member_c() << endl;
}
