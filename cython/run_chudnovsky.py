#!/usr/bin/python

import chudnovsky_pi

def main():
    for idx in xrange(0, 2):
        num = float(chudnovsky_pi.chudnovsky_num(idx))
        den = chudnovsky_pi.chudnovsky_denom(idx)
        print num, den
        term = chudnovsky_pi.calc_chudnovsky_pi(idx)
        print term
        print idx, num, den, den/num/12., term
        #print idx, chudnovsky_pi.calc_chudnovsky_pi(idx)

if __name__ == '__main__':
    main()
