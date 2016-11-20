#!/usr/bin/env python
#-*- coding: utf-8 -*-

import random
import StringIO
import packet

def put(args, data):
    did = data['pkt'].get('id')
    fname = data['pkt'].get('name')
    fname = "%s-%s" % (did, fname)
    
    args['svlock'].acquire()
    servers = args['sv']
    args['svlock'].release()

    server = random.sample(servers.values(), 1)[0]
    cli = args['svlink'](server, args['defaults']['domain'])

    sio = StringIO.StringIO(data['pkt'].get())
    cli.put(fname, sio)
    cli.commit()

    fid = args['db'].get_file_id(fname)
    args['db'].add_file(did, fid)

    pkt = packet.Packet({'result': 'OK'})
    data['sock'].sendall(pkt.tostr())

def get(args, data):
    fid = data['pkt'].get('id')
    fname = args['db'].get_file_name(fid)

    servers = args['db'].get_file_sv()
    output = StringIO.StringIO()
    if client.get(fname, output):
        output.seek(0)
        pkt = packet.Packet({'result': 'OK'}, output.read())
        data['sock'].sendall(pkt.tostr())
    else:
        pkt = packet.Packet({'result': 'Error'}, output.read())
        data['sock'].sendall(pkt.tostr())

def rm(args, data):
    fid = data['pkt'].get('id')
    fname = args['db'].get_file_name(fid)

    args['svlock'].acquire()
    servers = args['sv']
    args['svlock'].release()

    server = random.sample(servers.values(), 1)[0]
    cli = args['svlink'](server, args['defaults']['domain'])
    cli.delete(fname)
    cli.commit()

    pkt = packet.Packet({'result': 'OK'}, output.read())
    data['sock'].sendall(pkt.tostr())
