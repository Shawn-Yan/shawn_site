__author__ = 'shawn'

from tornado import ioloop, web, httpserver
from tornado.options import options, define
from multiprocessing import RLock
from pathlib import Path

from _db import *
from views import *

sub_path = Path(__file__).parent.joinpath
db_path = Path(__file__).parent / 'db.SQLite3'

MEDIA_DIR = Path(__file__).parent / 'media'
IMAGE_DIR = MEDIA_DIR / 'image'

#TODO
# design the handles with views
HANDLERS = [
    (r'/', HomeHandler),
    (r'/edit/$', ArticleEditHandler),
    (r'/article/([^/]+)', ArticleDetailHandler),
    (r'/outline/$', ArticleOutlineHandler),
]

UI_MODULES = {

}


class BlogApp(web.Application):
    def __init__(self, options):

        settings = dict(
            blog_title=u"Shawn Blog",
            template_path=str(sub_path('templates')),
            static_path=str(sub_path('static')),
            ui_modules=UI_MODULES,
            image_dir=IMAGE_DIR,
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/auth/login",
            debug=True,
        )
        web.Application.__init__(self, HANDLERS, **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = MySQLite(str(db_path))


def main():
    define('port', default=8080, type=int, help='run on the given port')
    options.parse_command_line()
    app = BlogApp(options)

    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)

    ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()

