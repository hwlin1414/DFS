#!/usr/bin/env python
#-*- coding: utf-8 -*-

import log
import logging

import random
import string
import StringIO
import packet

logger = logging.getLogger(__name__)

def put(args, data):
    did = data['pkt'].get('id')
    name = data['pkt'].get('name')
    #fname = "%s-%s" % (did, fname)

    rname = args['db'].get_file_rname(did, name)
    if rname is None:
        rname = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(32))
    logger.info("put did:%s \"%s\" rname: %s", did, name, rname)
    
    args['svlock'].acquire()
    servers = args['sv']
    args['svlock'].release()

    server = random.sample(servers.values(), 1)[0]
    cli = args['svlink'](server, args['defaults']['domain'])

    sio = StringIO.StringIO(data['pkt'].get())
    cli.put(rname, sio)
    cli.commit()

    fid = args['db'].get_file_id(rname)
    args['db'].add_file(did, fid, name)

    pkt = packet.Packet({}, 'OK')
    data['sock'].sendall(pkt.tostr())

def get(args, data):
    fid = data['pkt'].get('id')
    fname = args['db'].get_file_rname_by_id(fid)

    servers = args['db'].get_file_sv(fid)
    if servers == {}:
        logger.error("get (%s)%s ERROR - No Server", fid, fname)
        args['db'].rm_file(fid)
        pkt = packet.Packet({'result': 'Error'})
        data['sock'].sendall(pkt.tostr())
        return
        
    server = random.sample(servers.values(), 1)[0]
    client = args['svlink'](server, args['defaults']['domain'])
    output = StringIO.StringIO()
    if client.get(fname, output):
        logger.info("get (%s)%s OK", fid, fname)
        output.seek(0)
        pkt = packet.Packet({'result': 'OK'}, output.read())
        data['sock'].sendall(pkt.tostr())
    else:
        logger.error("get (%s)%s ERROR - koboldfs", fid, fname)
        pkt = packet.Packet({'result': 'Error'}, output.read())
        data['sock'].sendall(pkt.tostr())

def mvfile(args, data):
    fid = data['pkt'].get('id')
    pdid = data['pkt'].get('pdid')
    name = data['pkt'].get('name')

    logger.info("mvfile fid:%s pdid:%s, name:\"%s\"", fid, pdid, name)

    if pdid is not None:
        args['db'].move_file(fid, pdid)
    if name is not None:
        args['db'].rename_file(fid, name)
    pkt = packet.Packet({}, 'OK')
    data['sock'].sendall(pkt.tostr())

def rm(args, data):
    fid = data['pkt'].get('id')
    fname = args['db'].get_file_rname_by_id(fid)

    logger.info("rm (%s) %s", fid, fname)
    args['svlock'].acquire()
    servers = args['sv']
    args['svlock'].release()

    server = random.sample(servers.values(), 1)[0]
    args['db'].rm_file(fid)

    cli = args['svlink'](server, args['defaults']['domain'])
    cli.delete(fname)
    cli.commit()

    pkt = packet.Packet({}, 'OK')
    data['sock'].sendall(pkt.tostr())
