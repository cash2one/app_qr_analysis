# coding=utf-8
from handlers.SingInHandler import *
from handlers.StatisticsHandler import *
url_patterns = [
    (r"/login", SignInHandler),
    (r"/index", IndexHandler),
    (r"/statistics", StatisticsHandler),
]
