#!/usr/bin/env python
#-*- coding: utf-8 -*-
import MySQLdb
import MySQLdb.cursors
import json
import datetime

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

    def getroot(self, domain):
        self.c.execute("select * from dirs where name = %s and dir_id is NULL", (domain, ))
        res = self.c.fetchone()
        if res is not None:
            return res['id']

        self.c.execute("insert into dirs(`name`, `dir_id`) value(%s, NULL)", (domain, ))
        self.c.execute("select * from dirs where name = %s and dir_id is NULL", (domain, ))
        res = self.c.fetchone()
        return res['id']

    def server_list(self, domain):
        sv = {}
        self.c.execute("""
            SELECT servers.id, servers.name, servers.host FROM servers
            INNER JOIN servers_domains ON servers.id = server_id
            INNER JOIN domains ON domain_id = domains.id
            WHERE domains.name = %s
            """, (domain,))
        res = self.c.fetchall()
        for r in res:
            sv[r['name']] = {'id': r['id'], 'name': r['name'], 'host': r['host']}
        return sv

    def server_failed(self, server):
        self.c.execute("""
            SELECT replicas.id, file_id FROM replicas
            INNER JOIN servers ON replicas.server_id = servers.id
            WHERE servers.name = %s
        """, (server, ))
        res = self.c.fetchall()
        
        for r in res:
            print "found file: %d on %s" % (r['file_id'], server)
            self.c.execute("""
                DELETE FROM replicas
                WHERE id = %s
            """, (r['id'], ))
            self.c.execute("""
                UPDATE files SET replicas = replicas - 1
                WHERE id = %s
            """, (r['file_id'], ))

    def add_file(self, d, f):
        self.c.execute("""
            INSERT INTO files_dirs(file_id, dir_id)
            VALUE(%s, %s)
        """, (f, d))

    def get_file_sv(self, f):
        sv = {}
        self.c.execute("""
            SELECT servers.id, servers.name, servers.host FROM servers
            INNER JOIN replicas ON servers.id = server_id
            WHERE replicas.file_id = %s
            """, (f, ))
        res = self.c.fetchall()
        for r in res:
            sv[r['name']] = {'id': r['id'], 'name': r['name'], 'host': r['host']}
        return sv

    def get_file_name(self, fid):
        self.c.execute("""
            SELECT `key` FROM files
            WHERE id = %s
            """, (fid, ))
        res = self.c.fetchone()
        return res['key']

    def get_file_id(self, fname):
        self.c.execute("""
            SELECT `id` FROM files
            WHERE `key` = %s
            """, (fname, ))
        res = self.c.fetchone()
        return res['id']

    def rm_file(self, f):
        self.c.execute("""
            DELETE FROM files_dirs
            WHERE file_id = %s
        """, (f, ))

    def add_dir(self, d, name):
        self.c.execute("""
            INSERT INTO dirs(name, dir_id)
            VALUE(%s, %s)
        """, (name, d))

    def list_dir(self, d):
        ret = {}
        self.c.execute("""
            SELECT * FROM dirs
            WHERE id = %s
        """, (d, ))
        s = self.c.fetchone()
        if s is None: return ret
        ret['.'] = {'id': s['id'], 'name': '.', 'ctime': s['created_at'].strftime("%Y-%m-%d %H:%M:%S"), 'type': 'dir'}
        
        if s['dir_id'] is None:
            ret['..'] = {'id': s['id'], 'name': '..', 'ctime': s['created_at'].strftime("%Y-%m-%d %H:%M:%S"), 'type': 'dir'}
        else:
            self.c.execute("""
                SELECT * FROM dirs
                WHERE id = %s
            """, (s['dir_id'], ))
            sl = self.c.fetchone()
            ret['..'] = {'id': sl['id'], 'name': '..', 'ctime': sl['created_at'].strftime("%Y-%m-%d %H:%M:%S"), 'type': 'dir'}

        self.c.execute("""
            SELECT * FROM dirs
            WHERE dir_id = %s
        """, (s['id'], ))
        res = self.c.fetchall()
        for r in res:
            ret[r['name']] = {'id': r['id'], 'name': r['name'], 'ctime': r['created_at'].strftime("%Y-%m-%d %H:%M:%S"), 'type': 'dir'}

        return ret

    def list_file(self, d):
        ret = {}
        self.c.execute("""
            SELECT files.id, files.key, files.bytes, files.checksum, files.created_on
            FROM files
            INNER JOIN files_dirs ON files.id = files_dirs.file_id
            WHERE files_dirs.dir_id = %s
        """, (d, ))
        res = self.c.fetchall()
        for r in res:
            ret[r['key']] = {'id': r['id'], 'name': r['key'], 'size': r['bytes'], 'cksum': r['checksum'], 'ctime': r['created_on'].strftime("%Y-%m-%d %H:%M:%S"), 'type': 'file'}
        return ret

    def rm_dir(self, d):
        self.c.execute("""
            UPDATE dirs SET deleted_at = NOW()
            WHERE id = %s
        """, (d, ))

    def dir_path(self, d):
        pass
        
