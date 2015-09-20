# coding=utf-8
import pyqrcode
from settings import BASE_URL, MEDIA_ROOT
from custom_except import *
import os

"""
for generate qr code
need: pip install pyqrcode
      pip install PyPNG

"""

def qr_generator(code, scale=8):
    if not isinstance(code, str):
        if not isinstance(code, unicode):
            raise QrErrorException("内容格式不正确")

    content = BASE_URL + "app/" + code
    file_path = MEDIA_ROOT + "/qrcode/"
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    file_path = file_path + code + ".png"
    qrcode = pyqrcode.create(content, error="L")
    qrcode.png(file_path, scale=10, quiet_zone=1)
    web_path = "/static/qrcode/" + code + ".png"
    return web_path

if __name__ == "__main__":
    abc = qr_generator('fdafs321')
    print abc

