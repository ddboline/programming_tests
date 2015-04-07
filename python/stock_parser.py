#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import multiprocessing
from bs4 import BeautifulSoup
from urllib2 import urlopen

def read_stock_url(symbol):
    for line in urlopen("http://finance.yahoo.com/q?s=" + symbol.lower() + "&ql=0"):
        line = unicode(line, errors='ignore')
        if 'yfs_l84_%s' % symbol.lower() in line:
            price = float(line.split('yfs_l84_%s\">' % symbol.lower())[1].split('</')[0].replace(',',''))
            return symbol.upper(), price
    return symbol.upper(), -1

def write_output_file(price_q):
    with open('stock_prices.csv', 'w') as outfile:
        outfile.write('Stock,Price\n')
        while True:
            while not price_q.empty():
                try:
                    s, p = price_q.get()
                except TypeError:
                    return
                outfile.write('%s,%s\n' % (s, p))
            outfile.flush()

def run_stock_parser():
    price_q = multiprocessing.Queue()
    
    stock_symbols = []
    with open('symbols.txt','r') as symfile:
        for n, line in enumerate(symfile):
            sym = line.strip()
            if sym:
                stock_symbols.append(sym)
    pool = multiprocessing.Pool(5)
    output = multiprocessing.Process(target=write_output_file, args=(price_q,))
    output.start()
    
    for symbol, price in pool.imap_unordered(read_stock_url, stock_symbols):
        price_q.put([symbol, price])
    price_q.put(None)
    output.join()
    pool.close()
    pool.join()

if __name__ == '__main__':
    run_stock_parser()
