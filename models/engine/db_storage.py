#!/usr/bin/python3
""" Manages DBstorage Class """
from sqlalchemy.orm import sessionmaker, scoped_session, Session
from sqlalchemy import (create_engine)
from models.base_model import Base
from models.amenity import Amenity
from models.review import Review
from models.state import State
from models.place import Place
from os import getenv as env
from models.user import User
from models.city import City


class DBStorage():
    """ Class for logic of the DataBase """
    __engine = None
    __session = None

    def __init__(self):
        """ Definition of the inital method. """
        user = env("HBNB_MYSQL_USER")
        passwd = env("HBNB_MYSQL_PWD")
        host = env("HBNB_MYSQL_HOST")
        db = env("HBNB_MYSQL_DB")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)
        if env("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ Returns the dictionary of all current objects. """
        objDict = {}
        if cls:
            query = self.__session.query(cls).all()
            for obj in query:
                strKey = "{}.{}".format(type(obj).__name__, obj.id)
                objDict[strKey] = obj

        else:
            classList = ["Amenity", "Review", "State", "Place", "User", "City"]
            for className in classList:
                obj = self.__session.query(eval(className)).all()
                strKey = "{}.{}".format(className, obj.id)
                setattr(objDict, strKey, obj)
        return (objDict)

    def new(self, obj):
        """ Adds a new object to session. """
        self.__session.add(obj)

    def save(self):
        """ Commits the current session to the DB. """
        self.__session.commit()

    def delete(self, obj=None):
        """ Deletes an object from the current session. """
        self.__session.delete(obj)

    def reload(self):
        """ Reloads the engine, session and objects. """
        Base.metadata.create_all(self.__engine)
        session = sessionmaker(expire_on_commit=False, bind=self.__engine)
        Session = scoped_session(session)
        self.__session = Session()

    def close(self):
        """ Close the session """
        self.__session.close()
