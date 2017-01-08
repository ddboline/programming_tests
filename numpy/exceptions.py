#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import numpy as np


def exception_example():
    while True:
        try:
            x = int(input('Please enter a number: '))
            break
        except ValueError:
            print('enter a number...')
        except Exception as e:
            print('EXCEPTION %s' % e)
            pass
        finally:
            pass
        return x


def print_sorted(collection):
    try:
        collection.sort()
    except AttributeError:
        pass
    print(collection)


def run_print_sorted():
    print_sorted(list(np.random.uniform(0., 1., 100)))

    print_sorted([a for a in 'powqeoposdj'])


def filter_name(name):
    try:
        name = name.encode('ascii')
    except UnicodeEncodeError as e:
        if name == 'Gaël':
            print('OK, Gaël')
        else:
            raise e
    return name


def run_filter():
    filter_name(u'Gaël')
    try:
        filter_name(u'Stéfan')
    except UnicodeEncodeError as exc:
        print(exc)


def achilles_arrow(x):
    if abs(x - 1) < 1e-3:
        raise StopIteration
    x = 1 - (1 - x)/2.
    return x


if __name__ == '__main__':
    x = 0
    while True:
        try:
            x = achilles_arrow(x)
        except StopIteration:
            break

    print(x)
    #exception_example()
    run_filter()
    run_print_sorted()
