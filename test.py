import socket
import select
import hashlib

import packet

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 4096))
s.setblocking(False)

""" login """
print 'send:'
pkt = packet.Packet({'controller': 'auth', 'action': 'login', 'psk': hashlib.md5('133221333123111').hexdigest()})
print pkt.tostr()
s.sendall(pkt.tostr())

print 'recv:'
ss = select.select([s], [], [])
for s in ss[0]:
    buf = s.recv(4096)
    pkt = packet.Packet.parse(None, buf)
    if pkt:
        print pkt.tostr()
    else:
        print pkt

#""" test """
#print 'send:'
#pkt = packet.Packet({'mod_name': 'segment', 'mod_func': 'store', 'name': 'test', 'len': 10, 'offset': 0}, 'hello')
#print pkt.tostr()
#s.sendall(pkt.tostr())
#
#pkt = packet.Packet({'mod_name': 'segment', 'mod_func': 'get', 'name': 'test', 'len': 5, 'offset': 0})
#print pkt.tostr()
#s.sendall(pkt.tostr())
#
#print 'recv:'
#ss = select.select([s], [], [])
#for s in ss[0]:
#    pkt = handle.getpkt(s)
#    if pkt:
#        print pkt.tostr()
#    else:
#        print pkt

s.close()
