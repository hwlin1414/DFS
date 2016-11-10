#!/usr/bin/env python
#-*- coding: utf-8 -*-

import koboldfs
import koboldfs.client

import ConfigParser
import argparse
import sys
import threading

import util
import backends
import server

#c = koboldfs.client.Client('demo', servers = ['localhost:999'])

cfgfile = ('dfs.conf', )

def get_backend(cfg):
    if 'backend' not in cfg['defaults']:
        print "no backend selected"
        sys.exit(1)
    if cfg['defaults']['backend'] not in cfg:
        print "backend not configured"
        sys.exit(1)
    if not hasattr(backends, cfg['defaults']['backend']):
        print "backend not found"
        sys.exit(1)
    dbconf = cfg[cfg['defaults']['backend']]
    del dbconf['__name__']
    backend = getattr(backends, cfg['defaults']['backend']).database(**dbconf)
    return backend.open(cfg['defaults']['domain'])

def linkserver(server, domain):
    cli = koboldfs.client.Client(domain, servers = [server['host']])
    return cli

def checkserver(args):
    if args['defaults']['debug']:
        print "checkserver thread start"
    intval = int(args['defaults']['interval'])
    while True:
        args['svlock'].acquire()
        servers = args['sv']
        args['svlock'].release()
        for s in servers.values():
            cli = linkserver(s, args['defaults']['domain'])
            if cli.ping() == False:
                print "%s: %s [%s]" % (s['name'], s['host'], util.red("failed"))
                args['db'].server_failed(s['name'])
                args['svlock'].acquire()
                del args['sv'][s['name']]
                args['svlock'].release()
        if args['exit'].wait(intval) == True:
            break
    if args['defaults']['debug']:
        print "checkserver thread exit"

def main(args):
    args['exit'] = threading.Event()
    args['sv'] = args['db'].server_list(args['defaults']['domain'])
    args['svlock'] = threading.RLock()
    for s in args['sv'].values():
        cli = linkserver(s, args['defaults']['domain'])
        if cli.ping() == False:
            print "%s: %s [%s]" % (s['name'], s['host'], util.red("failed"))
            sys.exit(1)
        print "%s: %s [%s]" % (s['name'], s['host'], util.green("OK"))
    chksvth = threading.Thread(target = checkserver, name = 'chksvth', args = (args, ))
    chksvth.daemon = True
    chksvth.start()

    try:
        server.main(args)
    except KeyboardInterrupt:
        print ""
        print "Caught KeyboardInterrupt, closing..."
        args['exit'].set()
        chksvth.join()
    if args['defaults']['debug']:
        print "main exited"

if __name__ == "__main__":
    cfg = {
        'listen': '0.0.0.0',
        'port': '4096',
    }
    Config = ConfigParser.ConfigParser(cfg, allow_no_value = True)
    for file in cfgfile:
        Config.read(file)
        if Config.has_section('defaults'):
            cfg = Config._sections
    del cfg['defaults']['__name__']

    parser = argparse.ArgumentParser(description = "DFS Server", prog = sys.argv[0])
    parser.add_argument('-l', dest = 'listen', help = "Listen interface")
    parser.add_argument('-p', dest = 'port', type = int, help = "Listen port")
    parser.add_argument('-d', dest = 'debug', action = "store_true", help = "Debug mode")
    parser.set_defaults(**cfg['defaults'])
    cfg['defaults'] = vars(parser.parse_args(sys.argv[1:]))
    if cfg['defaults']['debug']: print cfg['defaults']

    backend = get_backend(cfg)
    if backend is None: 
        print "backend error"
        sys.exit(1)
    cfg['db'] = backend
    try:
        main(cfg)
    except KeyboardInterrupt, e:
        print ""
        sys.exit(0)
