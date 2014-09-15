__author__ = 'shawn'

from tornado.web import RequestHandler


class HomeHandler(RequestHandler):
    def get(self):
        self.render('home.html', title='Home', name='Shawn')


class ArticleEditHandler(RequestHandler):
    def get(self):
        self.render('articles/article_edit.html', title='Writing a article')


class ArticleDetailHandler(RequestHandler):
    def get(self):
        self.render('articles/article_detail.html', title='Article detail')