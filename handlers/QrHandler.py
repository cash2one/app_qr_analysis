# coding=utf-8
import tornado.web
from handlers.base import BaseHandler
from common.strUtil import random_ascii_string
from common.qrcode import *
from settings import MEDIA_ROOT
import  datetime

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


class AppIndexHandler(BaseHandler):
    def get(self, qr_id):
        #TODO 保存浏览记录
        print qr_id
        qr = self.datastore.get_qr_by_code(qr_id)
        user_agent = self.request.headers.get('User-Agent')
        if user_agent.find('MicroMessenger') > 0:
            agent = "weixin"
            if user_agent.find('Android') > 0:
                self.datastore.save_ScanData(qr.id, datetime.datetime.now(), 1, 1)
            elif user_agent.find('iPhone') > 0:
                self.datastore.save_ScanData(qr.id, datetime.datetime.now(), 2, 1)
            else:
                pass
        elif user_agent.find('Android') > 0:
            agent = "android"
        elif user_agent.find('iPhone') > 0:
            agent = "ios"
        else:
            agent = "web"
        return self.render("mobile_main.html", agent=agent, qr_id=qr_id)

class DownloadAppHandler(BaseHandler):
    def get(self, qr_id):
        print qr_id
        #TODO 保存下载记录
        qr = self.datastore.get_qr_by_code(qr_id)
        self.datastore.save_Download(qr.id, datetime.datetime.now(), 1, 1)
        file = MEDIA_ROOT+ "/apk/genshuixue.apk"
        self.set_header ('Content-Type', 'application/vnd.android.package-archive')
        self.set_header ('Content-Disposition', 'attachment; filename=genshuixue.apk')
        with open(file, 'rb') as f:
            while True:
                data = f.read()
                if not data:
                    break
                self.write(data)
        self.finish()


