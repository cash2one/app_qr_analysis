# coding=utf-8


import tornado.web
from handlers.base import BaseHandler
from util.pagination import Pagination


class SignInHandler(BaseHandler):
    def get(self):
        if self.current_user:
            return self.redirect("/index")
        next = self.get_argument("next", "")
        self.render("login.html", next=next)

    def post(self):
        email = self.get_argument("email", None)
        password = self.get_argument("password", None)
        next = self.get_argument("next", None)
        # remember = self.get_argument("remember")
        user = self.datastore.checkUser(email, password)
        if not user:
            return self.render("login.html", error=u'用户名或密码错误')
        self.set_current_user(user.email, user.id, 1)
        if next:
            return self.redirect(next)
        return self.redirect("/index")


class LogoutHandler(BaseHandler):
    def get(self):
        self.clear_cookie('tulip_user')
        return self.redirect('/')


class IndexHandler(BaseHandler):
    # @tornado.web.authenticated
    # def get(self):
    #     page = int(self.get_argument("page", 1))
    #     if page < 1:
    #         page = 1
    #     count = int(self.get_argument("count", 5))
    #     menu = self.active_menu("pic")
    #     total_count = self.datastore.get_pic_content_count()
    #     msgs = self.datastore.getPicContents(page - 1, count)
    #     pagination = Pagination(page, count, total_count)
    #     return self.render("index.html", menu=menu, msgs=msgs, pagination=pagination)


    def get(self):
        menu = self.active_menu("pic")
        return self.render("index_demo.html", menu=menu)


class RedictHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        return self.redirect("/index")

class TestHandler(BaseHandler):
    def get(self):
        return self.render("test.html")
