#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import time
import socket

class OpenUnixSocketServer(object):
    def __init__(self, socketfile=None, host=None, portno=None):
        self.sock = None
        self.socketfile = socketfile
        self.host = host
        self.portno = portno
        if socketfile and os.path.exists(socketfile):
            os.remove(socketfile)
        return

    def __enter__(self):
        if self.socketfile:
            net_type = socket.AF_UNIX
            addr_obj = self.socketfile
        else:
            net_type = socket.AF_INET
            addr_obj = (self.host, self.portno)
        self.sock = socket.socket(net_type, socket.SOCK_STREAM)
        try:
            self.sock.bind(addr_obj)
            if self.socketfile:
                os.chmod(self.socketfile, 0o777)
        except:
            print('failed to open socket')
            time.sleep(10)
            return self.__enter__()
        print('open socket')
        self.sock.listen(0)
        return self.sock

    def __exit__(self, exc_type, exc_value, traceback):
        self.sock.shutdown(socket.SHUT_RDWR)
        self.sock.close()
        if exc_type or exc_value or traceback:
            return False
        else:
            return True


class OpenSocketConnection(object):
    def __init__(self, sock):
        self.sock = sock

    def __enter__(self):
        self.conn, _ = self.sock.accept()
        return self.conn

    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()
        if exc_type or exc_value or traceback:
            return False
        else:
            return True


def main():
    try:
        portno = int(os.sys.argv[1])
    except ValueError:
        print('./server.py <port number>')
        exit(0)
    host = 'localhost'
    with OpenUnixSocketServer(host=host, portno=portno) as sock:
        while 1:
            with OpenSocketConnection(sock) as conn:
                dump = conn.recv(1024).decode()
                if not dump or dump.find('q') >= 0:
                    break
                print("Here is the message: %s" % dump)
                conn.send(dump.encode())
    return 0

if __name__ == '__main__':
    main()
