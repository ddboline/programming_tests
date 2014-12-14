#!/usr/bin/python

import multiprocessing
from bs4 import BeautifulSoup
from urllib2 import urlopen
    
def read_stock_url( symbol ):
    for line in urlopen("http://finance.yahoo.com/q?s=" + symbol.lower() + "&ql=0"):
        if 'yfs_l84_%s' % symbol.lower() in line:
            price = float( line.split('yfs_l84_%s\">' % symbol.lower())[1].split('</')[0].replace(',','') )
            return symbol.upper() , price
    return symbol.upper() , -1

def run_stock_parser():
    stock_symbols = []
    with open('symbols.txt','r') as symfile:
        for n , line in enumerate(symfile):
            sym = line.strip()
            if sym:
                stock_symbols.append( sym )
    pool = multiprocessing.Pool(5)
    for symbol , price in pool.imap_unordered( read_stock_url , stock_symbols ):
        print symbol, price

if __name__ == '__main__':
    run_stock_parser()
