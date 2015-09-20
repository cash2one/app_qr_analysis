#coding=utf-8
import os
import sys
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
"""
if there is any questions please see http://docs.sqlalchemy.org/en/latest/orm/tutorial.html
"""

# 单独执行时，把上级目录加入sys.path
ROOT = os.path.dirname(os.path.abspath(__file__))
fitPath = os.path.dirname(ROOT)
if fitPath not in sys.path:
    sys.path.append(fitPath)

from settings import DATABASE_NAME, HOST, PASSWORD, USER
ConnectString = "mysql://%s:%s@%s/%s?charset=utf8" % (USER,
                                                      PASSWORD,
                                                      HOST,
                                                      DATABASE_NAME)
print ConnectString
engine = create_engine(ConnectString,pool_recycle=7200,echo=False)
Base = declarative_base()

#####test#####
class test(Base):
    __tablename__ = "app_qr_test"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer)

    def __repr__(self):
        return "<test('%s')>" % (self.id)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_name = Column(String(50))
    password = Column(String(50))
    is_admin = Column(Boolean)
    is_active = Column(Boolean)
    last_login = Column(TIMESTAMP, default=datetime.utcnow())

    def __repr__(self):
        return "<User('{0}', '{1}')>".format(self.id, self.user_name)

class Qr(Base):
    __tablename__ = "app_qr_qr"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String(45))
    code = Column(String(50))
    qr_code = Column(String(50))
    create_time = Column(TIMESTAMP, default=datetime.now())
    create_user = Column(Integer)
    status = Column(Boolean)

class ScanHistory(Base):
    __tablename__ = "app_qr_scanHistory"
    id = Column(Integer, autoincrement=True, primary_key=True)
    qr_id = Column(Integer,ForeignKey('app_qr_qr.id'))
    createtime = Column(DATETIME)
    type = Column(Integer)
    count = Column(Integer)

class Download(Base):
    __tablename__ = "app_qr_download"
    id = Column(Integer, autoincrement=True, primary_key=True)
    qr_id = Column(Integer,ForeignKey('app_qr_qr.id'))
    createtime = Column(DATETIME)
    type = Column(Integer)
    count = Column(Integer)

Base.metadata.create_all(engine)



































