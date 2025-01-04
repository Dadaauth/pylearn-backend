"""MODULE Documentation"""
import os

from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker, scoped_session

from app.models.base import Base

# Make sure every ORM mapped model is imported here
# before calling Base.metadata.create_all()
from app.models.user import Admin, Student
from app.models.project import Project, StudentProject
from app.models.module import Module
from app.models.leaderboard import LeaderBoard
from app.models.notification import Notification
from app.models.point import Point
from app.models.streak import Streak


DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING")
TEST_DB_CONNECTION_STRING = os.environ.get("TEST_DB_CONNECTION_STRING")
DEVELOPMENT = os.getenv("ENVIRONMENT", "production").lower() == 'development'  # True or False


class DBStorage:
    """CLASS Documentation here"""
    
    __engine = None
    __session = None

    def __init__(self) -> None:
        self.testing = True if os.getenv("TESTING") == "True" else False
        self.__engine = create_engine(TEST_DB_CONNECTION_STRING if
                                      self.testing else DB_CONNECTION_STRING, echo=True, pool_pre_ping=True)
        self.reload()

    def drop_tables(self):
        """
            !!!!!!!!!
                Dangerous Area, Do not use this method in production
            !!!!!!!!!
        """
        if self.testing:
            self.__session.close()
            Base.metadata.drop_all(self.__engine)
        else:
            raise Exception("SafeGuard: Do not try to drop tables randomly in production!!!!")

    def reload(self) -> None:
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine)
        Session = scoped_session(session)
        self.__session = Session()

    def new(self, obj):
        try:
            self.__session.add(obj)
        except Exception as e:
            print("Exception Occured When working with DataBase", e)
            self.__session.rollback()
            return False

    def delete(self, obj):
        try:
            self.__session.delete(obj)
        except Exception as e:
            print("Exception Occured When working with DataBase", e)
            self.__session.rollback()
            return False

    def all(self, cls):
        try:
            return [obj for obj in self.__session.scalars(select(cls)).all()]
        except Exception as e:
            print("Exception Occured When working with DataBase", e)
            self.__session.rollback()
            return []
    
    def count(self, cls):
        try:
            return self.__session.query(cls).count()
        except Exception as e:
            print("Exception Occured When working with DataBase", e)
            self.__session.rollback()
            return False
    
    def search(self, cls, **filters):
        try:
            sh =  [obj for obj in self.__session.scalars(select(cls).filter_by(**filters))]
            return sh[0] if len(sh) == 1 else sh if len(sh) > 1 else None
        except Exception as e:
            print("Exception Occured When working with DataBase", e)
            self.__session.rollback()
            return False

    def save(self) -> None:
        try:
            self.__session.commit()
            return True
        except Exception as e:
            print("Exception Occured When Saving To DataBase", e)
            self.__session.rollback()
            return False

    def refresh(self, obj) -> None:
        self.__session.refresh(obj)

    def close(self) -> None:
        """Closes the Session object:: The
        connection to the database is hereby closed"""
        self.__session.close()

