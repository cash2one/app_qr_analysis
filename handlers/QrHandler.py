# coding=utf-8
import tornado.web
from handlers.base import BaseHandler
from common.strUtil import random_ascii_string
from common.qrcode import *

"""
module for qr_code request
"""

__author__ = 'jinlong'
__date__ = "2015-09-20"


class QrCodeAddHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        menu = self.active_menu("QrManage")
        return self.render("qr_add.html", menu=menu)

    @tornado.web.authenticated
    def post(self):
        code = self.get_argument("code")
        qr_code = self.get_argument("qr_code")
        channel_name = self.get_argument("channel_name")
        try:
            self.datastore.save_qr(code, qr_code, channel_name, self.current_user)
            self.write_success("保存成功")
        except Exception, e:
            print e
            self.write_except("保存失败, 请稍后重试")




class GenerateCodeHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        code = random_ascii_string(16)
        return self.write_success(code)


class GenerateQrCodeHandler(BaseHandler):
    @tornado.web.authenticated
    def post(self):
        code = self.get_argument("code")
        try:
            qr_code_uri = qr_generator(code)
            return self.write_success(qr_code_uri)
        except Exception, e:
            return self.write_except(e.message)



