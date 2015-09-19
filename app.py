#!/usr/bin/env python
import sys

import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import options
from settings import settings
from urls import url_patterns

class TornadoBoilerplate(tornado.web.Application):
    def __init__(self):
        #self.redis = Redis.instance()
        tornado.web.Application.__init__(self, url_patterns,**settings)

def main(port=options.port):
    app = TornadoBoilerplate()
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(port)
    print 'server running at', port
    tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    print sys.argv
    if len(sys.argv)==1:
        print 'run tornado with config file'
        main()
    elif len(sys.argv)==2:
        port=sys.argv[1]
        if port:
           main(port)
        else:
            print 'args error'
    else:
        print 'more args error'
