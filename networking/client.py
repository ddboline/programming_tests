#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import socket

class OpenUnixSocketClient(object):
    def __init__(self, host=None, portno=None, socketfile=None):
        self.sock = None
        self.socketfile = None
        self.host = host
        self.portno = portno
        if socketfile:
            self.socketfile = socketfile
    
    def __enter__(self):
        stm_type = socket.SOCK_STREAM
        if self.socketfile:
            net_type = socket.AF_UNIX
            addr_obj = self.socketfile
        else:
            net_type = socket.AF_INET
            addr_obj = (self.host, self.portno)
        self.sock = socket.socket(net_type, stm_type)
        try:
            err = self.sock.connect(addr_obj)
        except socket.error:
            return None
        if err:
            print(err)
        return self.sock

    def __exit__(self, exc_type, exc_value, traceback):
        self.sock.close()
        if exc_type or exc_value or traceback:
            return False
        else:
            return True


def main():
    if len(os.sys.argv) < 3:
        print("usage %s hostname port\n" % os.sys.argv[0])
        exit(1)
    host = os.sys.argv[1]
    port = int(os.sys.argv[2])
    with OpenUnixSocketClient(host, port) as sock:
        msg = ' '.join(os.sys.argv[3:])
        sock.send(msg.encode())
        msg = sock.recv(1024).decode()
        print(msg)
    return 0

if __name__ == '__main__':
    main()
