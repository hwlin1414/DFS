#!/usr/bin/env python
#-*- coding: utf-8 -*-

import socket
import select

import packet
import controller

def handle2(args, data):
    bef = None
    try:
        con = getattr(controller, data['pkt'].get('controller'))
        try:
            bef = getattr(con, 'before')
        except AttributeError, e:
            bef = None
        act = getattr(con, data['pkt'].get('action'))
    except (AttributeError, TypeError), e:
        print "Unknown Pack Recieved:"
        print data['pkt'].tostr()
        return True

    if args['defaults']['debug']:
        print "packet: %s -> %s" % (data['pkt'].get('controller'), data['pkt'].get('action'))
        print data['pkt'].tostr()

    if bef is not None:
        ret = bef(args, data)
        if ret == False:
            return False
    return act(args, data)

def handle(args, data):
    if args['defaults']['debug']:
        print "recieved packet"
    buf = data['sock'].recv(4096)
    if len(buf) == 0:
        return False
    data['pkt'] = packet.Packet.parse(data['pkt'], buf)

    ret = data['pkt'].check()
    if ret == True:
        ret = handle2(args, data)
        data['pkt'] = None
        return not ret == False
    elif ret == None:
        data['pkt'] = None
        
    return True

def newsock(args, sock, addr):
    if args['defaults']['debug']:
        print "newsocket:", addr
    i = args['conn']['count']
    args['conn']['count'] = i + 1
    args['conn']['total'][i] = sock
    args['conn']['data'][i] = {'pkt': None, 'sock': sock, 'addr': addr, 'auth': False, 'index': i}

def getId(conn, sock):
    for s in conn['total']:
        if conn['total'][s] == sock:
            return s
    return None

def main(args):
    svsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    svsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    svsock.bind((args['defaults']['listen'], args['defaults']['port']))
    svsock.listen(socket.SOMAXCONN)

    conn = {'count': 1, 'total': {0: svsock}, 'listen': svsock, 'data': {}}
    args['conn'] = conn

    while True:
        socks = select.select(conn['total'].values(), [], [], 1)
        for sock in socks[0]:
            if sock == conn['listen']:
                nsock, fromaddr = sock.accept()
                newsock(args, nsock, fromaddr)
            else:
                i = getId(conn, sock)
                if i == None:
                    print "getId failed i: %d" % (i, )
                    continue
                data = conn['data'][i]
                try:
                    ret = handle(args, data)
                except socket.error, e:
                    ret = False
                if ret == False:
                    del conn['total'][i]
                    del conn['data'][i]
