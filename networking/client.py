import socket
import os

def main():
    if len(os.sys.argv) < 3:
        print "usage %s hostname port\n" % os.sys.argv[0]
        exit(1)
    s = socket.socket()
    err = s.connect_ex((os.sys.argv[1], int(os.sys.argv[2])))
    if err:
        print 'failed to open socket %s' % err
        exit(1)
    s.send(raw_input())
    print s.recv(1024)
    s.close()
    return 0

main()
