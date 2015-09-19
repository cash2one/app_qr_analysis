# coding=utf-8
from handlers.SingInHandler import *
url_patterns = [
    (r"/login", SignInHandler),
    (r"/index", IndexHandler),
]
