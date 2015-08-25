#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from contextlib import closing
import requests

def read_stock_url(symbol):
    urlname = 'http://finance.yahoo.com/q?s=' + symbol.lower() + \
              '&ql=0'
    with closing(requests.get(urlname, stream=True)) as url_:
        for line in url_.iter_lines():
            line = line.decode(errors='ignore')
            if 'yfs_l84_%s' % symbol.lower() in line:
                price = float(line.split('yfs_l84_%s\">' % symbol.lower())[1]\
                                  .split('</')[0].replace(',',''))
                return symbol, price
    return symbol, -1

def run_stock_parser():
    stock_symbols = []
    with open('symbols.txt','r') as symfile:
        for n, line in enumerate(symfile):
            sym = line.strip()
            if sym:
                stock_symbols.append(sym)

    with open('stock_prices.csv', 'w') as outfile:
        outfile.write('Stock,Price\n')
        for symbol, price in map(read_stock_url, stock_symbols):
            outfile.write('%s,%s\n' % (symbol, price))
            print('%s, %s' % (s, p))

if __name__ == '__main__':
    run_stock_parser()
