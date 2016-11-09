#!/usr/bin/env python
#-*- coding: utf-8 -*-

def before(args, data):
    if data['auth'] == False:
        return False

def echo(args, data):
    data['sock'].sendall(data['pkt'].tostr())
