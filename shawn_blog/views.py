__author__ = 'shawn'

from tornado.web import RequestHandler
import markdown
from tornado import web
import unicodedata
import re


class BaseHandler(RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get_current_user(self):
        user_id = self.get_secure_cookie("blog_user")
        if not user_id:
            return None
        return self.db.select_id_flag('authors', int(user_id))


class HomeHandler(BaseHandler):
    def get(self):
        self.render('home.html', title='Home', name='Shawn')


class ArticleEditHandler(BaseHandler):
    def get(self):
        id = self.get_argument("id", None)
        article = None
        if id:
            articles = self.db.select_id_flag('article', int(id))
            article = articles[0]
        self.render("edit.html", article=article)

    def post(self):
        id = self.get_argument("id", None)
        title = self.get_argument("title")
        text = self.get_argument("markdown")
        html = markdown.markdown(text)
        if id:
            articles = self.db.select_id_flag('article', int(id))
            if not articles:
                raise web.HTTPError(404)
            article = articles[0]
            slug = article['slug']
            self.db.update_article(title, text, html, id)
        else:
            slug = unicodedata.normalize("NFKD", title).encode(
                "ascii", "ignore")
            slug = re.sub(r"[^\w]+", " ", slug)
            slug = "-".join(slug.lower().strip().split())

            if not slug:
                slug = "article"
            while True:
                e = self.db.select_slug_flag('article', slug)
                if not e:
                    break
                slug += "-2"
            self.current_user_id = 1
            self.db.insert_article(self.current_user_id, title, slug, text, html)
        self.redirect("/article/" + slug)


class ArticleDetailHandler(BaseHandler):
    def get(self, slug):
        article = self.db.select_slug_flag('article', slug)
        self.render('detail.html', article=article[0])


class ArticleDeleteHandler(BaseHandler):
    def get(self):
        id = self.get_argument("id", None)
        self.db.delete('article', int(id))
        self.render('delete.html')


class ArticleOutlineHandler(BaseHandler):
    def get(self):
        articles = self.db.select('article')
        self.render('outline.html', articles=articles)
