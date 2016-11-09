#!/usr/bin/env python
#-*- coding: utf-8 -*-

import StringIO
import select

class Packet:
    def __init__(self, header = {}, body = ""):
        self.header = header
        self.body = body
    def set(self, header, value = None):
        if value is None:
            self.body = header
            self.set('content-length', len(header))
        else:
            self.header[header] = value
    def get(self, header = None):
        if header is None:
            return self.body
        elif header in self.header:
            return self.header[header]
        else:
            return None
    def tostr(self):
        s = ""
        for x in self.header:
            s += x + ': ' + str(self.header[x]) + "\n"
        s += "\n"
        s += self.body
        return s
    def check(self):
        l = self.get('content-length')
        if l == None:
            print "packet unknown"
            return None
        if l == len(self.get()):
            return True
        return False

    @staticmethod
    def parse(pkt, x):
        if pkt == None:
            pkt = Packet()
            buf = StringIO.StringIO(x)
            while True:
                tmp = buf.readline().rstrip()
                if tmp == "":
                    break
                tmp = tmp.split(":", 1)
                if len(tmp) == 2:
                    pkt.set(tmp[0], tmp[1].strip())
        pkt.set(pkt.get() + buf.read())
        return pkt
