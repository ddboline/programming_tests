#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from multiprocessing import Process, Queue
from contextlib import closing
import requests
try:
    requests.packages.urllib3.disable_warnings()
except AttributeError:
    pass

_sentinel = 'EMPTY'

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

    ncpu = len(filter(lambda x: x.find('processor')==0,
                      open('/proc/cpuinfo')
                      .read().split('\n')))

    pool = [Process(target=read_stock_worker,
                                    args=(symbol_q, price_q,))
                                    for _ in range(ncpu*2)]
    
    for p in pool:
        p.start()
    output = Process(target=write_output_file, args=(price_q,))
    output.start()
    
    with open('symbols.txt','r') as symfile:
        for n, line in enumerate(symfile):
            symbol = line.strip()
            if symbol:
                symbol_q.put(symbol)

    symbol_q.put(_sentinel)
    for p in pool:
        p.join()
    price_q.put(_sentinel)
    output.join()

if __name__ == '__main__':
    run_stock_parser()
