#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

from multiprocessing import Pool, cpu_count
from contextlib import closing
import requests


def read_stock_url(symbol):
    urlname = 'http://finance.yahoo.com/q?s=' + symbol.lower() + '&ql=0'
    with closing(requests.get(urlname, stream=True)) as url_:
        for line in url_.iter_lines():
            line = line.decode(errors='ignore')
            if 'yfs_l84_%s' % symbol.lower() in line:
                price = line.split('yfs_l84_%s\">' % symbol.lower())[1]
                price = float(price.split('</')[0].replace(',', ''))
                return symbol, price
    return symbol, -1


def read_stock_url_thread(symbol, price_q):
    sym, price = read_stock_url(symbol)
    price_q.put((sym, price))
    return


def run_stock_parser():
    stock_symbols = []
    with open('symbols.txt', 'r') as symfile:
        for n, line in enumerate(symfile):
            sym = line.strip()
            if sym:
                stock_symbols.append(sym)

    ncpu = cpu_count()

    pool = Pool(ncpu * 4)

    stock_prices = []
    for symbol, price in pool.map(read_stock_url, stock_symbols):
        stock_prices.append((symbol, price))

    with open('stock_prices.csv', 'w') as outfile:
        outfile.write('Stock,Price\n')
        for symbol, price in stock_prices:
            outfile.write('%s,%s\n' % (symbol, price))


if __name__ == '__main__':
    run_stock_parser()
