#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 16:37:10 2015

@author: ddboline
"""
from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import eventlet
from flask import Flask, jsonify
from logging import getLogger

eventlet.monkey_patch()

app = Flask(__name__)
log = getLogger()

_strings = {}
with open('random_strings.txt', 'r') as inpf:
    for line in inpf:
        idx, rstr = line.split()[:2]
        _strings[int(idx)] = rstr


# straight from flask documentation
class Error(Exception):

    def __init__(self, message, status_code, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['msg'] = self.message
        return rv


class BadInputs(Error):
    def __init__(self, message, payload=None):
        Error.__init__(self, message, 400, payload)


def background(index):
    try:
        return jsonify({'string': _strings[index]}), 200
    except Error as e:
        raise e


@app.errorhandler(BadInputs)
def handle_bad_inputs(error):
    log.error('BAD INPUTS: ' + error.message)
    return jsonify(error.to_dict()), 400


class Internal(Error):
    def __init__(self, message, payload=None):
        Error.__init__(self, message, 500, payload)


@app.errorhandler(Internal)
def handler_internal(error):
    log.error('INTERNAL: ' + error.message)
    return jsonify(error.to_dict()), 500


@app.route('/randomstr/<int:index>', methods=['GET'])
def return_random_string(index):
    greenth = eventlet.spawn(backround, index)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=18603)
