# coding=utf-8
from handlers.QrHandler import *
from handlers.SignInHandler import *
from handlers.StatisticsHandler import *

url_patterns = [

    (r"/", IndexHandler),
    (r"/login", SignInHandler),
    (r"/logout", LogoutHandler),
    (r"/index", IndexHandler),
    (r"/statistics", StatisticsHandler),

    (r"/qr/add", QrCodeAddHandler),
    (r"/qr/generate/code", GenerateCodeHandler),
    (r"/qr/generate/qrcode", GenerateQrCodeHandler),
]
