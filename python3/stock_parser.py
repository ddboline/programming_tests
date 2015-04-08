#!/usr/bin/python3
# -*- coding: utf-8 -*-

import multiprocessing
from bs4 import BeautifulSoup
from urllib.request import urlopen

def read_stock_url(symbol_q, price_q):
    while True:
        while not symbol_q.empty():
            symbol = symbol_q.get()
            if symbol == 'EMPTY':
                return True
            for line in urlopen("http://finance.yahoo.com/q?s=" + symbol.lower() + "&ql=0"):
                line = str(line)
                if 'yfs_l84_%s' % symbol.lower() in line:
                    price = float(line.split('yfs_l84_%s\">' % symbol.lower())[1].split('</')[0].replace(',',''))
                    price_q.put((symbol.upper(), price))

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

def run_stock_parser():
    symbol_q = multiprocessing.Queue()
    price_q = multiprocessing.Queue()
    
    stock_symbols = []
    with open('symbols.txt','r') as symfile:
        for n, line in enumerate(symfile):
            sym = line.strip()
            if sym:
                stock_symbols.append(sym)

    ncpu = len([x for x in open('/proc/cpuinfo').read().split('\n')\
                if x.find('processor') == 0])

    pool = [multiprocessing.Process(target=read_stock_url, args=(symbol_q, price_q,)) for _ in range(ncpu*2)]
    for p in pool:
        p.start()
    output = multiprocessing.Process(target=write_output_file, args=(price_q,))
    output.start()

    for symbol in stock_symbols:
        symbol_q.put(symbol)
    for p in pool:
        symbol_q.put('EMPTY')
    for p in pool:
        p.join()
    price_q.put('EMPTY')
    output.join()

if __name__ == '__main__':
    run_stock_parser()
