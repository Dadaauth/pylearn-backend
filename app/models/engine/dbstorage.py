"""MODULE Documentation"""
import os

from flask import g
from sqlalchemy import create_engine, or_, select
from sqlalchemy.orm import sessionmaker, scoped_session

from app.models.base import Base

# Make sure every ORM mapped model is imported here
# before calling Base.metadata.create_all()
from app.models.user import Admin, Student, Mentor, MentorCohort
from app.models.project import AdminProject, CohortProject, StudentProject
from app.models.module import Module
from app.models.leaderboard import LeaderBoard
from app.models.notification import Notification
from app.models.point import Point
from app.models.streak import Streak
from app.models.course import Course
from app.models.cohort import Cohort


DB_CONNECTION_STRING = os.environ.get("DB_CONNECTION_STRING")
TEST_DB_CONNECTION_STRING = os.environ.get("TEST_DB_CONNECTION_STRING")
DEVELOPMENT = os.getenv("ENVIRONMENT", "production").lower() == 'development'  # True or False


class DBStorage:
    """CLASS Documentation here"""
    
    __engine = None
    __Session = None

    def __init__(self) -> None:
        self.testing = True if os.getenv("TESTING") == "True" else False
        self.__engine = create_engine(TEST_DB_CONNECTION_STRING if
                                      self.testing else DB_CONNECTION_STRING,
                                      pool_recycle=3600, pool_pre_ping=True,
                                      pool_size=20, max_overflow=40)
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(bind=self.__engine)
        self.__Session = scoped_session(session)

    def drop_tables(self):
        """
            !!!!!!!!!
                Dangerous Area, Do not use this method in production
            !!!!!!!!!
        """
        if self.testing:
            if g.db_session.is_active:
                g.db_session.close()
            Base.metadata.drop_all(self.__engine)
        else:
            raise Exception("SafeGuard: Do not try to drop tables randomly in production!!!!")

    def load_session(self):
        return self.__Session()

    def close(self) -> None:
        """
            Closes the session object and removes Session from scoped_session::
                The connection to the database is hereby closed
        """
        g.db_session.close()
        self.__Session.remove()

    def new(self, obj):
        try:
            g.db_session.add(obj)
        except Exception as e:
            print("Exception Occured When working with DataBase", e)
            if g.db_session.is_active:
                g.db_session.rollback()
            return False

    def delete(self, obj):
        try:
            g.db_session.delete(obj)
        except Exception as e:
            print("Exception Occured When working with DataBase", e)
            if g.db_session.is_active:
                g.db_session.rollback()
            return False

    def all(self, cls):
        try:
            return [obj for obj in g.db_session.scalars(select(cls)).all()]
        except Exception as e:
            print("Exception Occured When working with DataBase", e)
            if g.db_session.is_active:
                g.db_session.rollback()
            return []
    
    def count(self, cls, **filters):
        try:
            conditions = []

            for key, value in filters.items():
                field = getattr(cls, key)

                if isinstance(value, tuple):
                    conditions.append(or_(*[field == v for v in value]))
                else:
                    conditions.append(field == value)

            return g.db_session.query(cls).filter(*conditions).count()
        except Exception as e:
            print("Exception Occured When working with DataBase", e)
            if g.db_session.is_active:
                g.db_session.rollback()
            return False
    
    def search(self, cls, **filters):
        try:
            conditions = []

            for key, value in filters.items():
                field = getattr(cls, key)

                if isinstance(value, tuple):
                    conditions.append(or_(*[field == v for v in value]))
                else:
                    conditions.append(field == value)
            sh =  [obj for obj in g.db_session.scalars(select(cls).filter(*conditions))]
            return sh[0] if len(sh) == 1 else sh if len(sh) > 1 else None
        except Exception as e:
            return None

    def save(self) -> None:
        try:
            g.db_session.commit()
            return True
        except Exception as e:
            print("Exception Occured When Saving To DataBase", e)
            if g.db_session.is_active:
                g.db_session.rollback()
            return False

    def refresh(self, obj) -> None:
        g.db_session.refresh(obj)
