# coding=utf-8


import tornado.web
from handlers.base import BaseHandler
from common.pagination import Pagination


class SignInHandler(BaseHandler):
    def get(self):
        if self.current_user:
            return self.redirect("/index")
        next = self.get_argument("next", "")
        self.render("login.html", next=next)

    def post(self):
        user_name = self.get_argument("email", None)
        password = self.get_argument("password", None)
        next_url = self.get_argument("next", None)
        user = self.datastore.check_user(user_name, password)
        if not user:
            return self.render("login.html", error=u'用户名或密码错误')
        self.set_current_user(user.user_name, user.id, 1)
        if next_url:
            return self.redirect(next_url)
        return self.redirect("/index")


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('app_qr_code')
        return self.redirect('/')


class IndexHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        menu = self.active_menu("QrManage")
        return self.render("index_demo.html", menu=menu)


class RedictHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        return self.redirect("/index")

class TestHandler(BaseHandler):
    def get(self):
        return self.render("test.html")
