#!/usr/bin/env python
#-*- coding: utf-8 -*-

import json
import packet

def list(args, data):
    did = data['pkt'].get('id')
    if did is None:
        did = args['db'].root
    x = args['db'].list_dir(did)
    x.update(args['db'].list_file(did))
    s = json.dumps(x)
    pkt = packet.Packet({}, s)

def add(args, data):
    did = data['pkt'].get('id')
    dname = data['pkt'].get('name')
    args['db'].add_dir(did, dname)

def rm(args, data):
    did = data['pkt'].get('id')
    args['db'].add_dir(did)
