#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import os

def main():
    portno = int(os.sys.argv[1])
    host = 'localhost'
    s = socket.socket()
    try:
        s.bind((host, portno))
    except socket.error:
        exit(1)
    s.listen(1)
    while 1:
        c, a = s.accept()
        d = c.recv(1024)
        if not d or d.find('q') >= 0:
            break
        print "Here is the message: %s" % d
        c.send(d)
        c.close()
    s.shutdown(socket.SHUT_RDWR)
    s.close()
    return 0

if __name__ == '__main__':
    try:
        pn = int(os.sys.argv[1])
    except ValueError:
        print './server.py <port number>'
        exit(0)
    main()
