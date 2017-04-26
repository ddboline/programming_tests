#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function, unicode_literals)

from multiprocessing import cpu_count
from eventlet import monkey_patch
from eventlet.greenpool import GreenPool
from contextlib import closing

monkey_patch()

import requests
try:
    requests.packages.urllib3.disable_warnings()
except AttributeError:
    pass
monkey_patch()


def read_stock_url(symbol):
    urlname = 'http://finance.yahoo.com/q?s=' + symbol.lower() + \
              '&ql=0'
    with closing(requests.get(urlname, stream=True)) as url_:
        for line in url_.iter_lines():
            line = line.decode(errors='ignore')
            if 'yfs_l84_%s' % symbol.lower() in line:
                price = line.split('yfs_l84_%s\">' % symbol.lower())[1]
                price = float(price.split('</')[0].replace(',', ''))
                return symbol, price
    return symbol, -1


def run_stock_parser():
    stock_symbols = []
    with open('symbols.txt', 'r') as symfile:
        for n, line in enumerate(symfile):
            sym = line.strip()
            if sym:
                stock_symbols.append(sym)

    ncpu = cpu_count()

    pool = GreenPool(ncpu * 4)

    stock_prices = []
    for symbol, price in pool.imap(read_stock_url, stock_symbols):
        stock_prices.append((symbol, price))

    with open('stock_prices.csv', 'w') as outfile:
        outfile.write('Stock,Price\n')
        for symbol, price in stock_prices:
            outfile.write('%s,%s\n' % (symbol, price))


if __name__ == '__main__':
    run_stock_parser()
