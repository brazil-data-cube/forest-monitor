# pylint: disable=E0239

from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base

from forest_monitor.config import getCurrentConfig


def getDatabase():
    database = create_engine(getCurrentConfig().SQLALCHEMY_DATABASE_URI)
    return database


class DBO():
    def save(self, commit=True):
        """
        Save and persists object in database
        """

        try:

            db = getDatabase()
            connection = db.connect()

            connection.add(self)
        except Exception as e:
            raise e
        finally:
            db.dispose()

    def delete(self):

        """
        Delete object from database.
        """

        try:
            db = getDatabase()
            connection = db.connect()

            connection.delete(self)
        except Exception as e:
            raise e
        finally:
            db.dispose()

    def get(self):

        """
        Delete object from database.
        """

        try:
            db = getDatabase()
            connection = db.connect()

            connection.get(self)

        except Exception as e:
            raise e
        finally:
            db.dispose()

    def put(self, data):

        """
        Delete object from database.
        """

        try:

            db = getDatabase()
            connection = db.connect()

            connection.put(self, data)
        except Exception as e:
            raise e
        finally:
            db.dispose()


class BaseModel(declarative_base(metadata=MetaData()), DBO):
    """
    Abstract class for ORM model.
    Injects both `created_at` and `updated_at` fields in table
    """
    __abstract__ = True

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def update(self, data):
        for key, value in data.items():
            print(key)
            setattr(self, key, value)
