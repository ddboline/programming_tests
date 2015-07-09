#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
PROBLEM:
Stock Runs: Devise an algorithm that, given an input matrix of non-negative decimal values representing the price of a stock over some historical time, will return the pair of points at which to buy and then sell each stock so as to maximize profit. (One cannot simply find the global max and subtract the global min.)

You are given a matrix of n_dates by m_stocks.  you can construct a 10 days by 5 stock matrix with "n = (np.random.random((250, 500))*50).round(2)"

output should be a list of buy,sell indicies.  e.g. for:
n = np.array([[33.55,  18.26,   5.97,  18.38,  18.88],
              [ 7.14,   6.9,  47.51,  22.6,  48.95],
              [19.72,  49.73,  14.06,  42.94,   0.94],
              [37.61,  38.57,  45.55,   7.3,  36.8],
              [ 2.47,  33.43,  47.14,   0.66,   9.06],
              [47.61,  48.25,  21.95,  38.62,  23.92],
              [ 8.27,  41.05,  30.81,   1.47,  44.42],
              [30.91,  25.42,  49.32,  14.81,  37.49],
              [21.81,  19.36,  45.95,  15.43,  13.9],
              [48.08,   7.2,  39.42,  27.94,  35.45]])

buy_sell(n)  ==  [(4, 9), (1, 2), (0, 7), (4, 5), (2, 6)]
"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import numpy as np

def buy_sell(inp_array):
    '''
        Find buy/sell trade which maximizes profit per stock
        input is array of stock prices
        columns are stocks
        rows are time increments
        return is list of (buy_index, sell_index) tuples
    '''
    out_array = []
    if inp_array.shape[0] < 2:
        raise Exception
    for stock_idx in range(inp_array.shape[1]):
        ### consider first two time periods
        buy_idx = 0
        sell_idx = 1
        min_buy_idx = np.argmin(inp_array[0:2, stock_idx])
        max_profit = inp_array[sell_idx, stock_idx] - \
                     inp_array[buy_idx, stock_idx]
        for time_idx in range(2, inp_array.shape[0]):
            test_sell_idx = time_idx
            if inp_array[time_idx-1, stock_idx] < \
                    inp_array[min_buy_idx, stock_idx]:
                min_buy_idx = time_idx-1
            if inp_array[test_sell_idx, stock_idx] - \
                    inp_array[min_buy_idx, stock_idx] > max_profit:
                sell_idx = test_sell_idx
                buy_idx = min_buy_idx
                max_profit = inp_array[sell_idx, stock_idx] - \
                             inp_array[buy_idx, stock_idx]
        out_array.append((buy_idx, sell_idx))
    return out_array

if __name__ == '__main__':
    test_set = np.array([[33.55,  18.26,   5.97,  18.38,  18.88],
                         [7.14,   6.9,  47.51,  22.6,  48.95],
                         [19.72,  49.73,  14.06,  42.94,   0.94],
                         [37.61,  38.57,  45.55,   7.3,  36.8],
                         [2.47,  33.43,  47.14,   0.66,   9.06],
                         [47.61,  48.25,  21.95,  38.62,  23.92],
                         [8.27,  41.05,  30.81,   1.47,  44.42],
                         [30.91,  25.42,  49.32,  14.81,  37.49],
                         [21.81,  19.36,  45.95,  15.43,  13.9],
                         [48.08,   7.2,  39.42,  27.94,  35.45]])

    print([(4, 9), (1, 2), (0, 7), (4, 5), (2, 6)])
    print(buy_sell(test_set))

    test_set = np.array([[ 26.97,   2.89,  15.82,  13.5,   17.75],
                         [ 10.42,   0.07,  21.98,  46.04,   6.54],
                         [ 19.82,   1.55,   8.19,  43.97,   5.36],
                         [ 30.41,   1.26,  33.15,  25.96,   2.31],
                         [ 16.75,  48.23,   0.4,    9.28,  32.68],
                         [ 17.45,  34.79,  23.59,  24.15,  48.04],
                         [ 10.34,  45.48,  37.39,  23.35,  26.31],
                         [  2.25,   8.94,   4.92,   6.42,  16.52],
                         [ 40.89,  40.36,  43.07,  33.94,  13.56],
                         [ 22.92,   6.37,  11.89,  38.31,  10.16]])

    print(buy_sell(test_set))

    test_set = (np.random.random((10, 5))*50).round(2)
    print((test_set*100).astype(int)/100.)

    print(buy_sell(test_set))
