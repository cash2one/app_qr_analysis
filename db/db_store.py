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

    def get_user_by_id(self, id):
        try:
            user = self.session.query(User).filter(User.id == id, User.is_active == 1).one()
            if user is not None:
                return user
            return None
        except Exception,e:
            print 'exception in id',e
            return None

    def check_user(self, user_name, password):
        pwd = md5(password)
        try:
            user = self.session.query(User).filter(User.user_name==user_name, User.password==pwd).one()
            return user
        except Exception, e:
            print e
            return None

    def queryQrs(self):
        sql = "select name from app_qr_qr"
        return self.session.execute(sql, {})

    def queryScanDataWithBeginAndEnd(self,beginDate=None,endDate=None,osType=None,qrType=None):
        if beginDate == None:
            beginDate = datetime.datetime.min
        if endDate == None:
            endDate = datetime.datetime.max

        if osType != "0" and qrType != "0":
            sql = "select sh.id,qr.name,sh.createtime,sh.type,sh.count from app_qr_scanHistory sh left join app_qr_qr qr on sh.qr_id = qr.id where createtime >= :beginDate and createtime <= :endDate and qr_id = :qrType and type = :osType"
            return self.session.execute(sql, {'beginDate': beginDate, 'endDate': endDate, 'osType': osType, 'qrType': qrType})
        elif osType != "0":
            sql = "select sh.id,qr.name,sh.createtime,sh.type,sh.count from app_qr_scanHistory sh left join app_qr_qr qr on sh.qr_id = qr.id where createtime >= :beginDate and createtime <= :endDate and type = :osType"
            return self.session.execute(sql, {'beginDate': beginDate, 'endDate': endDate, 'osType': osType})
        elif qrType != "0":
            sql = "select sh.id,qr.name,sh.createtime,sh.type,sh.count from app_qr_scanHistory sh left join app_qr_qr qr on sh.qr_id = qr.id where createtime >= :beginDate and createtime <= :endDate and qr_id = :qrType"
            return self.session.execute(sql, {'beginDate': beginDate, 'endDate': endDate, 'qrType': qrType})
        else:
            sql = "select sh.id,qr.name,sh.createtime,sh.type,sh.count from app_qr_scanHistory sh left join app_qr_qr qr on sh.qr_id = qr.id where createtime >= :beginDate and createtime <= :endDate"
            return self.session.execute(sql, {'beginDate': beginDate, 'endDate': endDate})

    def queryDownloadDataWithBeginAndEnd(self,beginDate=None,endDate=None,osType=None,qrType=None):
        if beginDate == None:
            beginDate = datetime.datetime.min
        if endDate == None:
            endDate = datetime.datetime.max

        if osType != "0" and qrType != "0":
            sql = "select dl.id,qr.name,dl.createtime,dl.type,dl.count from app_qr_download dl left join app_qr_qr qr on dl.qr_id = qr.id where createtime >= :beginDate and createtime <= :endDate and qr_id = :qrType and type = :osType"
            return self.session.execute(sql, {'beginDate': beginDate, 'endDate': endDate, 'osType': osType, 'qrType': qrType})
        elif osType != "0":
            sql = "select dl.id,qr.name,dl.createtime,dl.type,dl.count from app_qr_download dl left join app_qr_qr qr on dl.qr_id = qr.id where createtime >= :beginDate and createtime <= :endDate and type = :osType"
            return self.session.execute(sql, {'beginDate': beginDate, 'endDate': endDate, 'osType': osType})
        elif qrType != "0":
            sql = "select dl.id,qr.name,dl.createtime,dl.type,dl.count from app_qr_download dl left join app_qr_qr qr on dl.qr_id = qr.id where createtime >= :beginDate and createtime <= :endDate and qr_id = :qrType"
            return self.session.execute(sql, {'beginDate': beginDate, 'endDate': endDate, 'qrType': qrType})
        else:
            sql = "select dl.id,qr.name,dl.createtime,dl.type,dl.count from app_qr_download dl left join app_qr_qr qr on dl.qr_id = qr.id where createtime >= :beginDate and createtime <= :endDate"
            return self.session.execute(sql, {'beginDate': beginDate, 'endDate': endDate})

if __name__ == '__main__':
    pass
    # example for sqlalchemy
    # query self.session.query().filter().all()
    # add self.session.add(commentObj)
    # commit self.session.commit()
    # sql self.session.execute(sql1, {'pic_id': id})
    # update self.session.merge(picContent)
    # 事务: session.rollback() see also http://docs.sqlalchemy.org/en/rel_1_0/orm/session_transaction.html
