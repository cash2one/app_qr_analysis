# coding=utf-8
from PIL import Image
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
    logo_path = MEDIA_ROOT + "/images/logo.png"
    if not os.path.exists(file_path):
        os.mkdir(file_path)
    file_path = file_path + code + ".png"
    qrcode = pyqrcode.create(content, error="L")
    qrcode.png(file_path, scale=10, quiet_zone=1)
    web_path = "/static/qrcode/" + code + ".png"

    qr_file = Image.open(file_path)
    logo = Image.open(logo_path)

    img = qr_file.convert("RGBA")
    img_w, img_h = img.size
    factor = 5
    size_w = int(img_w / factor)
    size_h = int(img_h / factor)

    icon_w, icon_h = logo.size
    if icon_w > size_w:
        icon_w = size_w
    if icon_h > size_h:
        icon_h = size_h

    icon = logo.resize((icon_w, icon_h), Image.ANTIALIAS)
    w = int((img_w - icon_w) / 2)
    h = int((img_h - icon_h) / 2)
    icon = icon.convert("RGBA")
    img.paste(icon, (w, h), icon)

    img.save(file_path)

    return web_path

if __name__ == "__main__":
    qr_generator("12345")


