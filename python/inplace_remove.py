from __future__ import print_function

some_list = list(range(10))
print(some_list)
for item in some_list:
    print(item, some_list)
    some_list.remove(item)
print(some_list)
