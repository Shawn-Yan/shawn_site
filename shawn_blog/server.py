__author__ = 'shawn'

from tornado import ioloop, web, httpserver
from tornado.options import options, define
from multiprocessing import RLock
from pathlib import Path

from _db import *
from views import *

sub_path = Path(__file__).parent.joinpath


#TODO
# design the handles with views
HANDLERS = [
    (r'/', HomeHandler),
    (r'/edit', ArticleEditHandler),
    (r'/article/([^/]+)', ArticleDetailHandler),
    (r'/outline', ArticleOutlineHandler),
    (r'/delete', ArticleDeleteHandler),
    (r'/auth/login', AuthLoginHandler),
    (r'/auth/logout', AuthLogoutHandler),
]

UI_MODULES = {

}


class BlogApp(web.Application):
    def __init__(self, options):

        settings = dict(
            blog_title=u"Shawn's Blog",
            template_path=str(sub_path('templates')),
            static_path=str(sub_path('static')),
            ui_modules=UI_MODULES,
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/auth/login",
            debug=True,
        )
        web.Application.__init__(self, HANDLERS, **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = MySQLite()


def main():
    define('port', default=8080, type=int, help='run on the given port')
    options.parse_command_line()
    app = BlogApp(options)

    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)

    ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()

