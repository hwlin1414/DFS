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
        self.check(domain)
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

    def check(self, domain):
        self.c.execute("select * from dirs where name = %s and dir_id is NULL", (domain, ))
        res = self.c.fetchone()
        if res is None:
            print "creating top dir"
            self.c.execute("insert into dirs(`name`, `dir_id`) value(%s, NULL)", (domain, ))
