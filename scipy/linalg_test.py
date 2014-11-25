#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np
from scipy import linalg

def mat_inv_wrap( arr ) :
    try :
        return linalg.inv( arr )
    except linalg.LinAlgError :
        return 'Singular Matrix'

def first() :
    #arr = np.array( [[1,2],[3,4]] )
    #print linalg.det( arr )
    #iarr = mat_inv_wrap( arr )
    #print iarr
    #print np.dot( arr, iarr )
    #print np.allclose( np.dot( arr, iarr ) , np.eye(2) )
    #arr = np.array( [[3,2],[6,4]] )
    #print linalg.det( arr )
    #print mat_inv_wrap( arr )
    #print linalg.det(np.ones((4,4)))
    #print mat_inv_wrap(np.ones((4,4)))

    arr = np.arange(9).reshape(3,3) + np.diag([1,0,1])
    print arr
    uarr , spec , vharr = linalg.svd( arr )
    print uarr
    print spec
    print vharr
    
    sarr = np.diag( spec )
    svd_mat = uarr.dot(sarr).dot(vharr)
    print svd_mat
    print np.allclose( svd_mat , arr )

    l , v = linalg.eig( arr )
    print l
    print v[:,0] , v[:,1] , v[:,2]
    print [ np.allclose( arr.dot(v[:,i])/l[i] , v[:,i] ) for i in range(3) ]

    #a = np.array( [ [ 1 , 0 ] , [ 1 , 3 ] ] )
    #l , v = linalg.eig( a )
    #print 'l',l
    #print 'v',v[:,0] , v[:,1]
    
    #b = a.dot(a)
    #l , v = linalg.eig( b )
    #print 'l',l
    #print 'v',v[:,0] , v[:,1]

    #u , s , v = linalg.svd( a )
    #print u
    #print s
    #print v
    

first()