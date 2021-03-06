import json
import logging
import os
from datetime import datetime, timedelta
from urllib.parse import urlencode

import jwt
import tornado.httpserver
import tornado.ioloop
import tornado.locks
import tornado.web
from tornado.httpclient import AsyncHTTPClient, HTTPClientError, HTTPRequest
from tornado.ioloop import IOLoop
from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)
define("secret", default=('changeit' if 'passwd' not in os.environ else os.environ.get('passwd')),
       help="key to encrypt jwt token", type=str)
url = "http://ids1.suda.edu.cn/amserver/UI/Login?goto=http://myauth.suda.edu.cn/default.aspx?app=eform"
url2 = "http://myauth.suda.edu.cn/default.aspx?app=eform"


class BrokerHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def prepare(self):
        if 'Content-Type' in self.request.headers and 'application/json' in self.request.headers['Content-Type']:
            self.args = json.loads(self.request.body.decode('utf8'))
        elif self.request.method == "OPTIONS":
            self.set_status(200)
            self.finish()
        else:
            self.set_status(status_code=412)
            self.write(json.dumps({"status": False, "data": "Expect json"}))
            self.finish()
        # Access self.args directly instead of using self.get_argument.

    def options(self):
        """
        对跨域 JSON 返回 OPTIONS 200
        :return:
        """
        self.set_status(200)
        self.finish()

    async def post(self):
        if self.args.get('id') and self.args.get('token'):
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            id_tag = self.args.get('id')
            token = self.args.get('token')

            http_client = AsyncHTTPClient()
            try:
                _ = await http_client.fetch(url, method="POST", headers=headers,
                                            body=urlencode({"IDToken1": id_tag, "IDToken2": token}),
                                            follow_redirects=False)
            except HTTPClientError as e:
                cookie = next(filter(lambda s: s.startswith(
                    'iPlanetDirectoryPro'), e.response.headers.get_list('Set-Cookie')))
                request = HTTPRequest(
                    url="http://myauth.suda.edu.cn/default.aspx?app=eform",
                    method='GET',
                    headers={
                        "Cookie": cookie,
                    },
                )
                response = await http_client.fetch(request)
                res = json.loads(response.body).get('data')
                res['exp'] = datetime.utcnow() + timedelta(days=3)
                user_token = jwt.encode(payload=res, key=options.secret, algorithm='HS256').decode('utf8')
                self.set_status(status_code=201)
                self.write(json.dumps({"code": 201, "message": user_token}))
                await self.finish()
            else:
                self.set_status(status_code=400)
                self.write(json.dumps(
                    {"code": 400, "message": "Authentication error"}))
                await self.finish()
        else:
            self.set_status(status_code=400)
            self.write(json.dumps({"code": 400, "message": "Wrong params"}))
            await self.finish()


class HealthcheckHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(status_code=200)
        self.write("ok")
        self.finish()


def make_app():
    tornado.options.parse_command_line()
    return tornado.web.Application([
        (r"/", BrokerHandler),
        (r"/healthcheck", HealthcheckHandler),
    ],
        # debug=True
    )


if __name__ == "__main__":
    tornado.options.parse_command_line()

    app = make_app()
    server = tornado.httpserver.HTTPServer(app)
    server.listen(options.port)
    if os.name == 'nt':
        server.start(1)
    else:
        server.start(0)  # forks one process per cpu
    logging.info("Tornado server listen at port :{}".format(options.port))
    logging.info("JWT encrypt secret is {}".format(options.secret))

    tornado.ioloop.IOLoop.current().start()
