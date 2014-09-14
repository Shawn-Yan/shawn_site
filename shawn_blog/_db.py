__author__ = 'shawn'

import sqlite3


class MySQLite:
    def __init__(self, path):
        self.conn = sqlite3.connect(path)
        self.cur = self.conn.cursor()

    def create(self, table):
        try:
            self.cur.execute("CREATE TABLE IF NOT EXISTS %s(Id INTEGER PRIMARY KEY AUTOINCREMENT,\
            Name VARCHAR(40),Flag INTEGER)" % table)
            self.done()
        except sqlite3.Error, e:
            print e
            self.conn.rollback()

    def insert(self, table, name, flag=0):
        try:
            self.cur.execute("INSERT INTO %s(Name,Flag) VALUES('%s',%d)" % (table, name, flag))
            self.done()
        except sqlite3.Error, e:
            print e
            self.conn.rollback()

    def drop(self, table):
        try:
            self.cur.execute("DROP TABLE IF EXISTS %s" % table)
            self.done()
        except sqlite3.Error, e:
            print e
            self.conn.rollback()

    def update(self, table, name, flag = 1):
        try:
            self.cur.execute("UPDATE %s SET Flag = %d WHERE Name = '%s'" % (table, flag, name))
            self.done()
        except sqlite3.Error, e:
            print e
            print 'SQLite3 update error'
            self.conn.rollback()

    def delete(self, table, name):
        try:
            self.cur.execute("DELETE FROM %s WHERE Name = '%s'" % (table, name))
            self.done()
        except sqlite3.Error, e:
            print e
            print 'SQLite3 delete error'
            self.conn.rollback()

    def select_flag(self, table, flag):
        try:
            self.cur.execute("SELECT * FROM %s WHERE Flag = %d" % (table, flag))
            rows = self.cur.fetchall()
            return rows
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]

    def select(self, table):
        try:
            self.cur.execute("SELECT * FROM %s" % table)
            rows = self.cur.fetchall()
            return rows
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]

    def done(self):
        self.conn.commit()

    def close(self):
        self.conn.close()