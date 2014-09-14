__author__ = 'shawn'

from tornado.web import RequestHandler


class HomeHandler(RequestHandler):
    def get(self):
        self.write("hello world")


def clear_marks(db, db_lock):
    with db_lock:
        db.marks.drop()

