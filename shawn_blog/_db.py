__author__ = 'shawn'

import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / 'db.SQLite3'


class MySQLite:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.cur = self.conn.cursor()

    def create(self, table, element):
        try:
            self.cur.execute("CREATE TABLE IF NOT EXISTS %s %s" % (table, element))
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

    def insert_article(self, author_id, title, slug, markdown, html):
        try:
            # self.cur.execute("INSERT INTO article (author_id,title,slug,markdown,html,published) "
            #                  "VALUES (%s,%s,%s,%s,%s,UTC_TIMESTAMP())"
            #                  % (author_id, title, slug, markdown, html))
            self.cur.execute("INSERT INTO article VALUES (%s,%s,%s,%s,%s,UTC_TIMESTAMP)"
                             % (author_id, title, slug, markdown, html))
            self.done()
        except sqlite3.Error, e:
            print e
            self.conn.rollback()

    def update_article(self, title, text, html, id):
        try:

            self.cur.execute("UPDATE article SET title = %s, markdown = %s, html = %s WHERE id = %s"
                             % (title, text, html, int(id)))
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

    def select_int_flag(self, table, str_flag, flag):
        try:
            self.cur.execute("SELECT * FROM %s WHERE %s = %d" % (table, str_flag, flag))
            rows = self.cur.fetchall()
            return rows
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]

    def select_str_flag(self, table, str_flag, flag):
        try:
            self.cur.execute("SELECT * FROM %s WHERE %s = %s" % (table, str_flag, flag))
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
