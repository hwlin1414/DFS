#!/usr/bin/env python
#-*- coding: utf-8 -*-

import log
import logging

import StringIO
import select

logger = logging.getLogger(__name__)

class Packet:
    def __init__(self, header = {}, body = "", nomodify = False):
        self.header = {}
        self.header.update(header)
        self.body = body
        if nomodify == False:
            self.set('content-length', len(body))
    def set(self, header, value = None, nomodify = False):
        if value is None:
            self.body = header
            if nomodify == False:
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
            logger.debug("packet check error(no content-length)")
            return None
        if int(l) <= len(self.get()):
            logger.debug("packet check ok")
            return True
        logger.debug("packet check false")
        #print "check false"
        return False

    @staticmethod
    def parse(pkt, x):
        buf = StringIO.StringIO(x)
        if pkt == None:
            pkt = Packet({}, "")
            while True:
                tmp = buf.readline().rstrip()
                if tmp == "":
                    break
                tmp = tmp.split(":", 1)
                if len(tmp) == 2:
                    pkt.set(tmp[0], tmp[1].strip())
        pkt.set(pkt.get() + buf.read(), nomodify = True)
        return pkt
