# -*- coding:utf-8 -*-
__author__ = 'shawn'

from tornado.web import RequestHandler
import html2text
from tornado import web, auth, escape
import unicodedata
import re
from datetime import datetime
import urllib
import json
import time
import os
from os.path import join, exists, getsize, getctime, splitext

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


class KeFileBrowseHandler(BaseHandler):
    def get(self):
        file_type = self.get_argument('dir')
        current_dir_path = self.get_argument('path', default='')
        file_type_allowed = []
        if file_type == "image":
            file_type_allowed = ['.jpg', '.gif', '.bmp', '.jpeg', '.png']
        elif file_type == "flash":
            file_type_allowed = ['.swf', '.flv']
        elif file_type == "media":
            file_type_allowed = ['.swf', '.flv', '.mp3', '.wav', '.wma', '.wmv', '.mid', '.avi', '.mpg', '.asf', '.rmvb']
        elif file_type == "file":
            file_type_allowed = ['.doc', '.docx', '.pdf', '.xls', '.xlsx', '.ppt', '.htm', '.html', '.txt', '.zip', '.rar', '.gz', '.bz2']

        root_path = join(self.settings['static_path'], 'media', current_dir_path)

        moveup_dir_path = ''
        file_list = []

        for name in os.listdir(root_path):
            file_dict = {}
            full_name = join(root_path, name).replace('\\', '/')
            file_dict['filename'] = name
            file_dict['filesize'] = getsize(full_name)
            file_dict['filetype'] = splitext(full_name)[1][1:]
            c_time = getctime(full_name)
            file_dict['datetime'] = str(datetime.fromtimestamp(c_time))[:-7]
            file_dict['has_file'] = (os.path.isdir(full_name) and len(os.listdir(full_name)) > 0)
            file_dict['is_dir'] = os.path.isdir(full_name)
            file_dict['is_photo'] = os.path.splitext(full_name)[1] in file_type_allowed

            file_list.append(file_dict)

        total_count = len(file_list)
        json_obj = {
            'current_url': r'/static/media/' + current_dir_path,
            'current_dir_path': current_dir_path,
            'moveup_dir_path': moveup_dir_path,
            'file_list': file_list,
            'total_count': total_count}

        self.write(json.dumps(json_obj, ensure_ascii=False))


class KeFileUploadHandler(BaseHandler):
    def post(self):
        file_type = self.get_argument('dir')
        imgFile = self.request.files['imgFile'][0]
        img_body = imgFile['body']

        if len(img_body) > (1024 * 1024 * 5):
            self.write(json.dumps(
                    {'error': 1, 'message': 'allow the 5M or less'}
                , ensure_ascii=False))
            return
        file_type_allowed = []
        if file_type == "image":
            file_type_allowed = ['.jpg', '.gif', '.bmp', '.jpeg', '.png']
        elif file_type == "flash":
            file_type_allowed = ['.swf', '.flv']
        elif file_type == "media":
            file_type_allowed = ['.swf', '.flv', '.mp3', '.wav', '.wma', '.wmv', '.mid', '.avi', '.mpg', '.asf', '.rmvb']
        elif file_type == "file":
            file_type_allowed = ['.doc', '.docx', '.pdf', '.xls', '.xlsx', '.ppt', '.htm', '.html', '.txt', '.zip', '.rar', '.gz', '.bz2']


        root_path = self.settings['static_path'] + '/media/'+file_type+'/'
        current_url = r'/static/media/'+file_type+'/'

        # dir name is base on time format like %Y%m%d
        t_datetime = datetime.fromtimestamp(time.time()).strftime('%Y%m%d')
        dir_name = join(t_datetime[:4], t_datetime[4:6], t_datetime[6:])
        c_dir = join(root_path, dir_name)
        if not exists(c_dir):
            os.makedirs(c_dir)


        # file name is base on the absolute time
        filename = str(int(time.time()))
        file_ext = '.' + imgFile['filename'].split('.')[-1]
        filename += file_ext
        if file_ext not in file_type_allowed:
            self.write(json.dumps(
                {'error': 1, 'message': 'extension name not allowed'}, ensure_ascii=False))
            return

        temp_file = open(join(root_path, dir_name, filename).lower(), 'wb+')
        temp_file.write(img_body)
        temp_file.close()

        current_url += (dir_name + r"/" + filename).replace('\\', '/')
        self.write(json.dumps({'error': 0, 'url': current_url}))

    def get(self):
        print "image"


class SearchHandler(BaseHandler):
    def get(self, *args, **kwargs):
        search_text = self.get_argument('search_text')
        articles = []
        if not search_text:
            self.redirect("/")
        else:
            all_articles = self.db.select('article')
            for temp in all_articles:
                if search_text.lower() in temp['title'].lower():
                    articles.append(temp)
        self.render('search_result.html', articles=articles)