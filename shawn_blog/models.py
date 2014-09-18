__author__ = 'shawn'

from datetime import datetime


class Author:
    FIELDS = (
        ('name', str, 'Shawn Yan'),
        ('email', str, 'yanxjun1990@gmail.com'),
    )

    def __init__(self, db=None):
        self.db = db
        for field, type, default in self.FIELDS:
            self.__dict__[field] = default


class Comment:
    FIELDS = (
        ('name', str, ''),
        ('comment', str, ''),
    )

    def __init__(self, db=None):
        self.db = db
        for field, type, default in self.FIELDS:
            self.__dict__[field] = default


class Article:
    FIELDS = (
        ('id', int, 0),
        ('name', str, ''),
        ('content', str, ''),
        ('author', Author, None),
        ('date', datetime, datetime.now),
        ('comment', None, []),
    )

    def __init__(self, db=None):
        self.db = db
        for field, type, default in self.FIELDS:
            self.__dict__[field] = default


