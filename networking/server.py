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
    s.close()
    return 0

main()
