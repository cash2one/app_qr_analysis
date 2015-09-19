#coding=utf-8
import os
import json
import simplejson
import tornado.web
from mako.lookup import TemplateLookup
import db.db_store as db
from uuid import *


import logging
logger = logging.getLogger('boilerplate.' + __name__)

class BaseHandler(tornado.web.RequestHandler):
    """A class to collect common handlers methods - all other handlers should
    subclass this one.
    """
    @property
    def datastore(self):
        return db.datastore.instance()

    def active_menu(self, css):
        menu = {
            'pic': "",
            'Reports': "",
            'Analytics': "",
            'Export': ""
        }
        menu.update({css:'active'})
        return menu

    def get_body_param(self, name, defaultVal=None):
        data = simplejson.loads(self.request.body)
        return data.get(name, defaultVal)


    def set_current_user(self,user_email,user_id,remember):
        if user_id:
            if remember==1:
                self.set_secure_cookie("tulip_user", str(user_id), expires_days=60)
            else:
                self.set_secure_cookie("tulip_user", str(user_id), expires_days=2)
        else:
            self.clear_cookie("tulip_user")

    def get_current_user(self):
        user_id = self.get_secure_cookie("tulip_user")
        if user_id:
            user = self.datastore.getUserById(user_id)
            return user
        return None

    @property
    def lookup(self):
        myLookup = TemplateLookup([os.path.join(str(os.path.dirname('./templates')), 'templates').replace('\\','/'),],
                output_encoding='utf-8',
                encoding_errors='replace')
        return myLookup

    def render(self, template_name, **kwargs):
        """ Redefine the render """
        t = self.lookup.get_template(template_name)
        args = dict(
            handler=self,
            request=self.request,
            current_user=self.current_user,
            locale=self.locale,
            _=self.locale.translate,
            static_url=self.static_url,
            xsrf_form_html=self.xsrf_form_html,
            reverse_url=self.application.reverse_url,
            _xsrf = self.xsrf_token
        )
        args.update(kwargs)
        html = t.render(**args)
        self.finish(html)

    def get_uuid(self):
        return str(uuid4()).replace("-","")



    def write_json(self, obj):
        self.set_header("Content-Type", "application/json; charset=UTF-8")
        self.finish(json.dumps(obj))

    def load_json(self):
        """Load JSON from the request body and store them in
        self.request.arguments, like Tornado does by default for POSTed form
        parameters.

        If JSON cannot be decoded, raises an HTTPError with status 400.
        """
        try:
            self.request.arguments = json.loads(self.request.body)
        except ValueError:
            msg = "Could not decode JSON: %s" % self.request.body
            logger.debug(msg)
            raise tornado.web.HTTPError(400, msg)

    def get_json_argument(self, name, default=None):
        """Find and return the argument with key 'name' from JSON request data.
        Similar to Tornado's get_argument() method.
        """
        if default is None:
            default = self._ARG_DEFAULT
        if not self.request.arguments:
            self.load_json()
        if name not in self.request.arguments:
            if default is self._ARG_DEFAULT:
                msg = "Missing argument '%s'" % name
                logger.debug(msg)
                raise tornado.web.HTTPError(400, msg)
            logger.debug("Returning default argument %s, as we couldn't find "
                    "'%s' in %s" % (default, name, self.request.arguments))
            return default
        arg = self.request.arguments[name]
        logger.debug("Found '%s': %s in JSON arguments" % (name, arg))
        return arg
