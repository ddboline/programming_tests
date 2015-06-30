#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from eventlet import spawn, Queue
from eventlet import greenthread, monkey_patch
from contextlib import closing
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
                price = float(line.split('yfs_l84_%s\">' % symbol.lower())[1]\
                                  .split('</')[0].replace(',',''))
                return price
    return -1

def read_stock_worker(symbol_q, price_q):
    while True:
        while not symbol_q.empty():
            symbol = symbol_q.get()
            if symbol == 'EMPTY':
                return True
            price = read_stock_url(symbol)
            if price >= 0:
                price_q.put((symbol.upper(), price))
            greenthread.sleep()
        greenthread.sleep()
    return

def write_output_file(price_q):
    with open('stock_prices.csv', 'w') as outfile:
        outfile.write('Stock,Price\n')
        while True:
            while not price_q.empty():
                vals = price_q.get()
                if vals == 'EMPTY':
                    return True
                s, p = vals
                outfile.write('%s,%s\n' % (s, p))
                outfile.flush()
                greenthread.sleep()
            greenthread.sleep()

def run_stock_parser():
    symbol_q = Queue()
    price_q = Queue()
    
    stock_symbols = []
    with open('symbols.txt','r') as symfile:
        for n, line in enumerate(symfile):
            sym = line.strip()
            if sym:
                stock_symbols.append(sym)

    ncpu = len(filter(lambda x: x.find('processor')==0,
                      open('/proc/cpuinfo')
                      .read().split('\n')))

    pool = [spawn(read_stock_worker, symbol_q, price_q)
                                    for _ in range(ncpu*2)]
    output = spawn(write_output_file, price_q)

    for symbol in stock_symbols:
        symbol_q.put(symbol)
    for p in pool:
        symbol_q.put('EMPTY')
    for p in pool:
        p.wait()
    price_q.put('EMPTY')
    output.wait()

if __name__ == '__main__':
    run_stock_parser()
