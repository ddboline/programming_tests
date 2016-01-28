#include <iostream>
#include <memory>

using namespace std;

struct node {
    int x;
    shared_ptr<node> prev;
    shared_ptr<node> next;
};

class doubly_linked_list {
public:
    doubly_linked_list() :
        root_node(new node)
    {
        root_node->x = 0;
        root_node->prev = nullptr;
        root_node->next = nullptr;
        current_node = root_node;
    };
    doubly_linked_list(const doubly_linked_list& x){
        root_node = x.root_node;
        current_node = x.current_node;
    };
    ~doubly_linked_list() {};
    void add(int x) {
        shared_ptr<node> new_node(new node);
        new_node->x = x;
        new_node->prev = current_node;
        new_node->next = nullptr;
        current_node->next = new_node;
        current_node = new_node;
    }
    void remove_back() {
        shared_ptr<node> temp(current_node);
        current_node = current_node->prev;
    }
    void remove_front() {
        shared_ptr<node> temp(root_node);
        root_node = root_node->next;
    }
    void print_list() {
        shared_ptr<node> temp(root_node);
        while(temp) {
            cout << temp->x << " ";
            temp = temp->next;
        }
        cout << endl;
    }
    shared_ptr<node> begin() {return root_node;};
    shared_ptr<node> end() {return current_node;};
private:
    shared_ptr<node> root_node;
    shared_ptr<node> current_node;
};

shared_ptr<node> add_to_list(const shared_ptr<node> & current_node, int value) {
    if(!current_node)
        return current_node;
    shared_ptr<node> new_node(new node);
    shared_ptr<node> temp_node = current_node->next;
    current_node->next = new_node;
    if(temp_node) {
        temp_node->prev = new_node;
        new_node->next = temp_node;
    }
    new_node->prev = current_node;
    new_node->x = value;
    return new_node;
}

int recurse(int n){
    if(n > 100) {
        cout << "stop ";
        return n;
    }
    cout << "n " << n++ << " ";
    int val = recurse(n);
    cout << "val " << val << " ";
    return val;
};

int main() {
    shared_ptr<node> root(new node);
    root->next = nullptr;
    root->x = 5;
    shared_ptr<node> current_node(root);
    for(int i = 0; i<100; i++)
        current_node = add_to_list(current_node, i + 12);
    current_node = root;
    
    while(current_node) {
        cout << current_node->x << " ";
        current_node = current_node->next;
    }
    cout << endl;
    recurse(0);
    cout << endl;
    doubly_linked_list l;
    for(int i=0; i<100; i++)
        l.add(i*2);
    l.print_list();
}
