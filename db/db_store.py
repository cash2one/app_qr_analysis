# -*- coding=utf-8 -*-
"""
数据库操作
"""
import datetime
from db_session import DBOBJ
from db_model import *
from util.strUtil import md5


class datastore(object):
    def __init__(self):
        mydb = DBOBJ.instance()
        self.session = mydb.session

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    # def getUserById(self, id):
    #     self.session.close()
    #     try:
    #         user = self.session.query(User).filter(User.id == id, User.is_active == 1).one()
    #         if user is not None:
    #             return user
    #         return None
    #     except Exception,e:
    #         print 'exception in id',e
    #         return None
    #
    # def saveUser(self, userObj):
    #     self.session.close()
    #     try:
    #         self.session.add(userObj)
    #         self.session.commit()
    #     except Exception, e:
    #         print e
    #
    #
    # def checkUser(self, email, password):
    #     self.session.close()
    #     pwd = md5(password)
    #     try:
    #         user = self.session.query(User).filter(User.email==email, User.password==pwd).one()
    #         return user
    #     except Exception, e:
    #         print e
    #         return None

if __name__ == '__main__':
    pass
    # example for sqlalchemy
    # query self.session.query().filter().all()
    # add self.session.add(commentObj)
    # commit self.session.commit()
    # sql self.session.execute(sql1, {'pic_id': id})
    # update self.session.merge(picContent)
    # 事务: session.rollback() see also http://docs.sqlalchemy.org/en/rel_1_0/orm/session_transaction.html
