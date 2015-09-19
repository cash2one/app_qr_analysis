import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from settings import DATABASE_NAME, HOST, PASSWORD, USER


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
