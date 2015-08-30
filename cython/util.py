#!/usr/bin/python

from functools import wraps
def jit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper
