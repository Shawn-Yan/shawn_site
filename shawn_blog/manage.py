# -*- coding:utf-8 -*-
__author__ = 'shawn'

#TODO manage some work
# add author (me) to Author table
import sqlite3

con = sqlite3.connect("db.SQLite3")
cur = con.cursor()
cur.execute("INSERT INTO authors (name,email) VALUES('Shawn','yanxjun1990@gmail.com')")
con.commit()
con.close()

