import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.db_model import User
from settings import DATABASE_NAME, HOST, PASSWORD, USER
from common.strUtil import md5

__all__=['Singleton', 'DBOBJ']


class Singleton(object):
    """
    Singleton class
    """
    def __init__(self, decorated):
        self._decorated = decorated

    def instance(self, *args, **kwargs):
        try:
            return self._instance
        except AttributeError:
            self._instance = self._decorated(*args, **kwargs)
            return self._instance

    def __call__(self, *args, **kwargs):
        raise TypeError('Singletons must be accessed through the `Instance` method.')

@Singleton
class DBOBJ(object):
    """
    The DB Class should only exits once, thats why it has the @Singleton decorator.
    To Create an instance you have to use the instance method:
        db = Db.instance()
    """
    engine = None
    session = None
    def __init__(self):
        ConnectString = "mysql://%s:%s@%s/%s?charset=utf8" % (USER, PASSWORD, HOST, DATABASE_NAME)
        self.engine = create_engine(ConnectString, pool_size=100, pool_recycle=3600, echo=False, max_overflow=15)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def instance(self, *args, **kwargs):
        """
        Dummy method, cause several IDEs can not handel singeltons in Python
        """
        pass

def create_user(user_name, password, is_admin=1, is_active=1):
        user = User()
        user.user_name = user_name
        password = md5(password)
        user.password = password
        user.is_admin = is_admin
        user.is_active = is_active
        return user


if __name__ == "__main__":
    session = DBOBJ.instance().session
    user = create_user('admin', 'qr_code')
    session.add(user)
    session.commit()
