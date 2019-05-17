import logging
import os

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.ioloop import IOLoop
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)
define("key", default=('changeit' if 'passwd' not in os.environ else os.environ.get('passwd')),
       help="key to encrypt jwt token", type=str)


class BrokerHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")


def make_app():
    tornado.options.parse_command_line()
    return tornado.web.Application([
        (r"/", BrokerHandler),
    ],
        debug=True,
    )


if __name__ == "__main__":
    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.bind(options.port)
    if os.name == 'nt':
        server.start(1)
    else:
        server.start(0)  # forks one process per cpu
    logging.info("Tornado server listen at port :{}".format(options.port))
    IOLoop.current().start()
