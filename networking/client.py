#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import os

def main():
    s = socket.socket()
    err = s.connect_ex((os.sys.argv[1], int(os.sys.argv[2])))
    if err:
        print('failed to open socket %s' % err)
        exit(1)
    msg = ' '.join(os.sys.argv[3:])
    s.send(msg.encode())
    msg = s.recv(1024).decode()
    print(msg)
    s.close()
    return 0

if __name__ == '__main__':
    if len(os.sys.argv) < 3:
        print("usage %s hostname port\n" % os.sys.argv[0])
        exit(1)
    main()
