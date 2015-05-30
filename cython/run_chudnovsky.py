#!/usr/bin/python3

import pyximport
pyximport.install()

import chudnovsky_pi
import chudnovsky_pi1

def main():
    print(chudnovsky_pi.calc_chudnovsky_pi(0))
    print(chudnovsky_pi.calc_chudnovsky_pi(0))


    for idx in range(0, 2):
        num = float(chudnovsky_pi.chudnovsky_num(idx))
        den = chudnovsky_pi.chudnovsky_denom(idx)
        print(num, den)
        term = chudnovsky_pi.calc_chudnovsky_pi(idx)
        print(term)
        print(idx, num, den, den/num/12., term)

    return

if __name__ == '__main__':
    main()
