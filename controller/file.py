#!/usr/bin/env python
#-*- coding: utf-8 -*-

import packet
import util
import random
import StringIO

def put(args, data):
    did = data['pkt'].get('id')
    fname = data['pkt'].get('name')
    
    args['svlock'].acquire()
    servers = args['sv']
    args['svlock'].release()

    server = random.sample(servers.values(), 1)[0]
    cli = args['svlink'](server, args['defaults']['domain'])

    sio = StringIO.StringIO(data['pkt'].get())
    cli.put(fname, sio)
    cli.commit()
    args['db'].add_file(did, fid)

    pass
    
def get(args, data):
    args['db'].get_file_sv()
    pass

def rm(args, data):
    pass
