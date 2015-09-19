#coding=utf-8
import os
import sys
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

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

Base.metadata.create_all(engine)

































