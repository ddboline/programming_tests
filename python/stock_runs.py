#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np

def buy_sell_per_stock(inp_array):
    if len(inp_array) < 2:
        raise Exception
    ### consider first two elements first
    buy_index = 0
    sell_index = 1
    max_profit = inp_array[sell_index] - inp_array[buy_index]
    if len(inp_array) == 2:
        return (buy_index, sell_index)
    for index in range(2, len(inp_array)):
        ### now consider a sliding window starting with 1,2
        test_buy_index = index - 1
        test_sell_index = index
        ### if test_sell + current best buy increases profit, keep it
        if inp_array[test_sell_index] - inp_array[buy_index] > max_profit:
            sell_index = test_sell_index
            max_profit = inp_array[sell_index] - inp_array[buy_index]
        ### if test_sell + test_buy increases profit, keep both
        if inp_array[test_sell_index] - inp_array[test_buy_index] > max_profit:
            sell_index = test_sell_index
            buy_index = test_buy_index
            max_profit = inp_array[sell_index] - inp_array[buy_index]
    return (buy_index, sell_index)

def buy_sell(inp_array):
    out_array = []
    for stock_idx in range(inp_array.shape[1]):
        out_array.append(buy_sell_per_stock(inp_array[:, stock_idx].tolist()))
    return out_array

if __name__ == '__main__':
    test_set = np.array([[ 33.55,  18.26,   5.97,  18.38,  18.88],
                         [  7.14,   6.9 ,  47.51,  22.6 ,  48.95],
                         [ 19.72,  49.73,  14.06,  42.94,   0.94],
                         [ 37.61,  38.57,  45.55,   7.3 ,  36.8 ],
                         [  2.47,  33.43,  47.14,   0.66,   9.06],
                         [ 47.61,  48.25,  21.95,  38.62,  23.92],
                         [  8.27,  41.05,  30.81,   1.47,  44.42],
                         [ 30.91,  25.42,  49.32,  14.81,  37.49],
                         [ 21.81,  19.36,  45.95,  15.43,  13.9 ],
                         [ 48.08,   7.2 ,  39.42,  27.94,  35.45]])

    print([(4, 9), (1, 2), (0, 7), (4, 5), (2, 6)])
    print(buy_sell(test_set))

    test_set = (np.random.random((10, 5))*50).round(2)
    print((test_set*100).astype(int)/100.)

    print(buy_sell(test_set))
