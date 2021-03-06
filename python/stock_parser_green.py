#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from multiprocessing import cpu_count
from eventlet import spawn, Queue
from eventlet import monkey_patch
from contextlib import closing

monkey_patch()

import requests
try:
    requests.packages.urllib3.disable_warnings()
except AttributeError:
    pass

_sentinel = object()


def read_stock_url(symbol):
    urlname = 'http://finance.yahoo.com/q?s=' + symbol.lower() + \
              '&ql=0'
    with closing(requests.get(urlname, stream=True)) as url_:
        for line in url_.iter_lines():
            line = line.decode(errors='ignore')
            if 'yfs_l84_%s' % symbol.lower() in line:
                price = float(line.split('yfs_l84_%s\">' % symbol.lower())[1]\
                                  .split('</')[0].replace(',',''))
                return price
    return -1


def read_stock_worker(symbol_q, price_q):
    for symbol in iter(symbol_q.get, _sentinel):
        price = read_stock_url(symbol)
        if price >= 0:
            price_q.put((symbol.upper(), price))
    symbol_q.put(_sentinel)
    return True


def write_output_file(price_q):
    with open('stock_prices.csv', 'w') as outfile:
        outfile.write('Stock,Price\n')
        for vals in iter(price_q.get, _sentinel):
            s, p = vals
            outfile.write('%s,%s\n' % (s, p))
            outfile.flush()
    return True


def run_stock_parser():
    symbol_q = Queue()
    price_q = Queue()

    stock_symbols = []
    with open('symbols.txt', 'r') as symfile:
        for n, line in enumerate(symfile):
            sym = line.strip()
            if sym:
                stock_symbols.append(sym)

    ncpu = cpu_count()

    pool = [spawn(read_stock_worker, symbol_q, price_q) for _ in range(ncpu * 2)]
    output = spawn(write_output_file, price_q)

    for symbol in stock_symbols:
        symbol_q.put(symbol)
    symbol_q.put(_sentinel)
    for p in pool:
        p.wait()
    price_q.put(_sentinel)
    output.wait()


if __name__ == '__main__':
    run_stock_parser()
