#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Wed Apr 13 10:21:32 2016

@author: ddboline
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)
import gurobipy as gp


def basic():
    m = gp.Model()
    
    m.ModelName = 'My Second Model'

    x = m.addVar(name='x')
    y = m.addVar(name='y')
    z = m.addVar(name='z')
    
    m.update()

    m.setObjective(2*x + y + z, gp.GRB.MAXIMIZE)
    
    m.addConstr(x + 2*y + z <= 4, name='c0')
    m.addConstr(x - y == 0, name='c1')
    m.addConstr(x >= 0, name='c2')
    m.addConstr(y >= 0, name='c3')
    m.addConstr(z >= 0, name='c4')
    
    m.update()
    
    m.write('basic.lp')
    
    m.optimize()
    
    print(m)
    
    m.printStats()
    
    for var in x, y, z:
        print(var.VarName, var.X)

    return
    
if __name__ == '__main__':
    basic()