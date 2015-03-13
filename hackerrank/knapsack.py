# Enter your code here. Read input from STDIN. Print output to STDOUT
import random

import numpy as np

def knapsack(arr, k):
    min_diff = k%arr[0]
    arr_dict = {}
    mod_dict = {}
    for a in arr:
        kmoda = k%a
        if kmoda < min_diff:
            min_diff = kmoda
        if min_diff == 0:
            break
        if a <= k:
            arr_dict[a] = kmoda
            mod_dict[kmoda] = a
    if min_diff == 0:
        print k
        return
    for a in arr_dict:
        if a in mod_dict:
            print k
            return
    print k-min_diff
    print sorted(arr_dict.keys())
    print sorted(arr_dict.values())



n = random.randint(1,2000)
arr = [random.randint(1,2000) for x in range(n)]
k = random.randint(1,2000)
print k
knapsack(arr, k)

arrs = [[9, [3,2,4]],
        [12, [3,10,4]],
        [13, [3,10,4]],
        [16, [3,10,4]],
        [2000, [2000,2000,2000]]]

for k, arr in arrs:
    #print k
    knapsack(arr, k)
