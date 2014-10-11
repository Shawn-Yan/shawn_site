__author__ = 'shawn'

import sqlite3
from pathlib import Path

db_path = Path(__file__).parent / 'db.SQLite3'


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class MySQLite:
    def __init__(self):
        try:
            print(db_path)
            self.conn = sqlite3.connect(str(db_path))
            self.conn.row_factory = dict_factory
            self.cur = self.conn.cursor()
            self.create_table_article()
            self.create_table_authors()
        except sqlite3.Error, e:
            print e, "init"

    def create_table_authors(self):
        try:
            self.cur.execute("CREATE TABLE authors"
                             "(id INTEGER PRIMARY KEY,"
                             "email VARCHAR(100) UNIQUE,"
                             "name VARCHAR(100))")

            self.done()
        except sqlite3.Error, e:
            print e, "create_table_authors"
            self.conn.rollback()

    def create_table_article(self):
        try:
            self.cur.execute("CREATE TABLE article"
                             "(id INTEGER PRIMARY KEY,"
                             "author_id INTEGER REFERENCES authors(id),"
                             "slug VARCHAR(100) UNIQUE,"
                             "title VARCHAR(512),"
                             "markdown MEDIUMTEXT,"
                             "html MEDIUMTEXT,"
                             "thumbnail MEDIUMTEXT,"
                             "type VARCHAR(10),"
                             "read_count INT,"
                             "published DATETIME,"
                             "updated TIMESTAMP)")
            self.done()
        except sqlite3.Error, e:
            print e, "create_table_article"
            self.conn.rollback()

    def drop(self, table):
        try:
            self.cur.execute("DROP TABLE IF EXISTS '%s'" % table)
            self.done()
        except sqlite3.Error, e:
            print e
            self.conn.rollback()

    def insert_article(self, author_id, title, slug, markdown, html, type, thumbnail):
        try:
            self.cur.execute("INSERT INTO article (author_id,title,slug,markdown,html,published,type,thumbnail)"
                             "VALUES ('%s','%s','%s','%s','%s',CURRENT_TIMESTAMP,'%s','%s')"
                             % (author_id, title, slug, markdown, html, type, thumbnail))
            self.done()
        except sqlite3.Error, e:
            print e, "insert_article error***"
            self.conn.rollback()

    def update_article(self, title, text, html, thumbnail, id):
        try:

            self.cur.execute("UPDATE article SET title = '%s', markdown = '%s', html = '%s', "
                             "thumbnail ='%s' WHERE id = '%s'"
                             % (title, text, html, thumbnail, int(id)))
            self.done()
        except sqlite3.Error, e:
            print e
            print 'SQLite3 update error'
            self.conn.rollback()

    def delete(self, table, flag):
        try:
            self.cur.execute("DELETE FROM %s WHERE id = '%d'" % (table, flag))
            self.done()
        except sqlite3.Error, e:
            print e
            print 'SQLite3 delete error'
            self.conn.rollback()

    def select_id_flag(self, table, flag):
        try:
            self.cur.execute("SELECT * FROM '%s' WHERE id = %d" % (table, flag))
            rows = self.cur.fetchall()
            return rows
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]

    def select_slug_flag(self, table, flag):
        try:
            self.cur.execute("SELECT * FROM '%s' WHERE slug = '%s'" % (table, flag))
            rows = self.cur.fetchall()
            return rows
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]

    def select_type_flag(self, table, flag):
        try:
            self.cur.execute("SELECT * FROM '%s' WHERE type = '%s'" % (table, flag))
            rows = self.cur.fetchall()
            return rows
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]

    def select(self, table):
        try:
            self.cur.execute("SELECT * FROM '%s'" % table)
            rows = self.cur.fetchall()
            return rows
        except sqlite3.Error, e:
            print "Error %s:" % e.args[0]

    def done(self):
        self.conn.commit()

    def close(self):
        self.conn.close()
