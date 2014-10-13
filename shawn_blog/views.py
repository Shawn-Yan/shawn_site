# -*- coding:utf-8 -*-
__author__ = 'shawn'

from tornado.web import RequestHandler
import html2text
from tornado import web, auth, escape
import unicodedata
import re
from datetime import datetime
import urllib

# no.1 is for me
author_id = 1
max_len = 200


class BaseHandler(RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("blog_author")
        if not user_id:
            return None
        author = self.db.select_id_flag('authors', int(author_id))
        return author


class HomeHandler(BaseHandler):
    def get(self):
        articles = self.db.select('article')
        self.render('home.html', articles=articles)


class ArticleEditHandler(BaseHandler):
    @web.authenticated
    def get(self):
        id = self.get_argument("id", None)
        article = None
        if id:
            articles = self.db.select_id_flag('article', int(id))
            article = articles[0]
        self.render("edit.html", article=article)

    @web.authenticated
    def post(self):
        id = self.get_argument("id", None)
        title = self.get_argument("title")
        html = self.get_argument("markdown")
        text = html2text.html2text(html)
        type = self.get_argument("type")
        text_len = len(text)
        if text_len > max_len:
            thumbnail = text[0:max_len]
        else:
            thumbnail = text
        if id:
            articles = self.db.select_id_flag('article', int(id))
            if not articles:
                raise web.HTTPError(404)
            article = articles[0]
            slug = article['slug']
            self.db.update_article(title, text, html, thumbnail, id)
        else:
            slug = unicodedata.normalize("NFKD", title).encode(
                "ascii", "ignore")
            slug = re.sub(r"[^\w]+", " ", slug)
            slug = "-".join(slug.lower().strip().split())

            if not slug:
                slug = urllib.quote(title.encode('utf8'))

            while True:
                e = self.db.select_slug_flag('article', slug)
                if not e:
                    break
                slug += "-2"
            self.current_user_id = 1
            self.db.insert_article(self.current_user_id, title, slug, text, html, type, thumbnail)
        self.redirect("/article/" + slug)


class ArticleDetailHandler(BaseHandler):
    def get(self, slug):
        slug = urllib.quote(slug.encode('utf8'))
        article = self.db.select_slug_flag('article', slug)
        article_date = article[0]['published']
        art_date = datetime.strptime(article_date, "%Y-%m-%d %H:%M:%S")
        self.render('detail.html', article=article[0], art_date=art_date)


class ArticleDeleteHandler(BaseHandler):
    def get(self):
        id = self.get_argument("id", None)
        self.db.delete('article', int(id))
        self.render('delete.html')


class ArticleOutlineHandler(BaseHandler):
    def get(self):
        articles = self.db.select('article')
        self.render('outline.html', articles=articles)


class AuthLoginHandler(BaseHandler):
    # @web.asynchronous
    def get(self):
        if not self.current_user:
            self.render('login.html')
        else:
            self.redirect(self.get_argument(next), "/")

    # @web.asynchronous
    def post(self):
        name = self.get_argument('name', None)
        password = self.get_argument('password', None)
        if name == "yanxjun" and password == "19900913343x":
            print("the name and password is correct!")
            self.set_secure_cookie("blog_author", str(author_id))
        self.redirect("/")


class AuthLogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie("blog_author")
        self.redirect(self.get_argument("next", "/"))


class ArticleTypeHandler(BaseHandler):
    def get(self, type_):
        table = "article"
        articles = self.db.select_type_flag(table, type_)
        self.render('type.html', articles=articles, type_=type_)


class AboutMeHandler(BaseHandler):
    def get(self):
        self.render('about_me.html')

