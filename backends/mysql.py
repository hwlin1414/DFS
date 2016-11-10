#!/usr/bin/env python
#-*- coding: utf-8 -*-
import MySQLdb
import MySQLdb.cursors
import json

class database(object):
    def __init__(self, host='localhost', port='3306', user=None, passwd=None, db=None):
        self.host = host
        self.port = port
        self.user = user
        self.passwd = passwd
        self.db = db

    def open(self, domain):
        try :
            db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, port=int(self.port), cursorclass=MySQLdb.cursors.DictCursor)
        except MySQLdb.Error, e:
            print "DB connection Error %d: %s" % (e.args[0], e.args[1])
            return None
        db.autocommit(True)
        self.c = db.cursor()
        self.c.execute('set names \'utf8\'')
        self.root = self.getroot(domain)
        return self

    def server_list(self, domain):
        sv = {}
        self.c.execute("""
            SELECT servers.name, servers.host FROM servers
            INNER JOIN servers_domains ON servers.id = server_id
            INNER JOIN domains ON domain_id = domains.id
            WHERE domains.name = %s
            """, (domain,))
        res = self.c.fetchall()
        for r in res:
            sv[r['name']] = {'name': r['name'], 'host': r['host']}
        return sv

    def getroot(self, domain):
        self.c.execute("select * from dirs where name = %s and dir_id is NULL", (domain, ))
        res = self.c.fetchone()
        if res is not None:
            return res['id']

        self.c.execute("insert into dirs(`name`, `dir_id`) value(%s, NULL)", (domain, ))
        self.c.execute("select * from dirs where name = %s and dir_id is NULL", (domain, ))
        res = self.c.fetchone()
        return res['id']

    def add_file(self, d, f):
        pass
    def rm_file(self, f):
        pass
    def add_dir(self, d, name):
        pass
    def list_dir(self, d):
        pass
    def list_file(self, d):
        pass
    def rm_dir(self, d):
        pass
