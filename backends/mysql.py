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

    def open(self):
        try :
            db = MySQLdb.connect(host=self.host, user=self.user, passwd=self.passwd, db=self.db, port=int(self.port), cursorclass=MySQLdb.cursors.DictCursor)
        except MySQLdb.Error, e:
            print "DB connection Error %d: %s" % (e.args[0], e.args[1])
            return None
        db.autocommit(True)
        self.c = db.cursor()
        self.c.execute('set names \'utf8\'')
        #self.check()
        return self
    def server_list(self, domain):
        self.c.execute("""
            select servers.name, servers.host from servers
            inner join servers_domains on servers.id = server_id
            inner join domains on domain_id = domains.id
            where domains.name = %s
            """, (domain,))
        res = self.c.fetchall()
        return res
#    def check(self):
#        self.c.execute('show tables')
#        res = self.c.fetchall()
#        if len(res) == 0 or res[0]['Tables_in_imc'] != 'main':
#            self.c.execute('create table main(`k` varchar(64) not null primary key, `v` varchar(1024) not null);')
#
#    def get(self, key, default = None):
#        self.c.execute("select v from main where k = %s", (key,))
#        res = self.c.fetchall()
#        if len(res) == 0: return default
#        return json.loads(res[0]['v'])
#
#    def set(self, key, val):
#        val = json.dumps(val)
#        self.c.execute("select k from main where k = %s", (key,))
#        res = self.c.fetchall()
#        if len(res) == 0:
#            self.c.execute("insert into main(k, v) value(%s, %s)", (key, val))
#        else:
#            self.c.execute("update main set v = %s where k = %s", (val, key))
#
#    def unset(self, key):
#        self.c.execute("delete from main where k = %s", (key,))
