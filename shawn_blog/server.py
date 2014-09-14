__author__ = 'shawn'

from tornado import ioloop, web, httpserver
from tornado.options import options, define
from multiprocessing import RLock
from pathlib import Path

from _db import *
from views import *

sub_path = Path(__file__).parent.joinpath
db_path = Path(__file__).parent

MEDIA_DIR = Path(__file__).parent / 'media'
IMAGE_DIR = MEDIA_DIR / 'image'

#TODO
# design the handles with views
HANDLERS = [
    (r'/', HomeHandler),
]

UI_MODULES = {

}


class BlogApp(web.Application):
    def __init__(self, options):
        db_lock = RLock()
        super.__init__(
            handlers=HANDLERS,
            template_path=str(sub_path('templates')),
            static_path=str(sub_path('static')),
            ui_modules=UI_MODULES,
            db=MySQLite(db_path),
            db_lock=db_lock,
            image_dir=IMAGE_DIR,
            debug=True,
            # autoreload=False,
        )


def main():
    define('port', default=8080, type=int, help='run on the given port')
    options.parse_command_line()
    app = BlogApp(options)

    http_server = httpserver.HTTPServer(app)
    http_server.listen(options.port)

    ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()

