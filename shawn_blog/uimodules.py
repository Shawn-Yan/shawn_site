__author__ = 'shawn'

from tornado import web
from datetime import datetime


class EntryModule(web.UIModule):
    def render(self, article):
        article_date = article['published']
        art_date = datetime.strptime(article_date, '%Y-%m-%d %H:%M:%S')
        return self.render_string("modules/article.html", article=article, art_date=art_date)