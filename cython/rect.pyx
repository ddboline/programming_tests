#!/usr/bin/python

cdef extern from 'rectangle.h' namespace 'shapes' :
    cdef cppclass rectangle :
        rectangle(int, int, int, int) except +
        int x0, y0, x1, y1
        int getLength()
        int getHeight()
        int getArea()
        void move(int, int)

def create_rectange() :        
    cdef rectangle *rec = new rectangle(1, 2, 3, 4)
    try:
        recLength = rec.getLength()
        ...
    finally:
        del rec     # delete heap allocated object

cdef class PyRectangle:
    cdef rectangle *thisptr      # hold a C++ instance which we're wrapping
    def __cinit__(self, int x0, int y0, int x1, int y1):
        self.thisptr = new rectangle(x0, y0, x1, y1)
    def __dealloc__(self):
        del self.thisptr
    def getLength(self):
        return self.thisptr.getLength()
    def getHeight(self):
        return self.thisptr.getHeight()
    def getArea(self):
        return self.thisptr.getArea()
    def move(self, dx, dy):
        self.thisptr.move(dx, dy)
