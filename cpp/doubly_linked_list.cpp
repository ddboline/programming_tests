#include <iostream>
// #include <forward_list>

using namespace std;

struct node {
    int x;
    node *next;
};

class doubly_linked_list {
public:
    doubly_linked_list() {};
    doubly_linked_list(int x) {
        root_node = new node;
        root_node->x = 0;
        root_node->next = nullptr;
        current_node = root_node;
    };
    ~doubly_linked_list() {
        while(root_node) {
            cout << "remove " << root_node->x << " ";
            remove();
        }
        cout << endl;
    }
    void add(int x) {
        node * temp_ = new node;
        temp_->x = x;
        temp_->next = nullptr;
        current_node->next = temp_;
        current_node = temp_;
    }
    void remove() {
        node * temp = root_node;
        root_node = root_node->next;
        delete temp;
    }
    void print_list() {
        node * temp = root_node;
        while(temp) {
            cout << temp->x << " ";
            temp = temp->next;
        }
        cout << endl;
    }
    node * begin() {return root_node;};
    node * end() {return current_node;};
private:
    node * root_node;
    node * current_node;
};

node * add_to_list(node * current_node, int value) {
    node *new_node = new node;
    current_node->next = new_node;
    new_node->next = nullptr;
    new_node->x = value;
    return new_node;
};

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
    node *root = new node;
    root->next = nullptr;
    root->x = 5;
    node *current_node = root;
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
    doubly_linked_list l(0);
    for(int i=0; i<100; i++)
        l.add(i*2);
    l.print_list();
}
