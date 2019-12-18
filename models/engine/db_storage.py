#!/usr/bin/python3
"""This is the file Dbstorage"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
import sqlalchemy as db
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session
from os import environ
from models.base_model import Base

class DBStorage:
    '''New Engine'''

    __engine = None
    __session = None

    def __init__(self):
        '''Constructor'''
        user = environ.get('HBNB_MYSQL_USER')
        password = environ.get('HBNB_MYSQL_PWD')
        host = environ.get('HBNB_MYSQL_HOST')
        database = environ.get('HBNB_MYSQL_DB')
        hbn_env = environ.get('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                           .format(user, password, host, database),
                           pool_pre_ping=True)
        if hbn_env == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None): 
        '''return a dictionary '''
        dictionary_to_return = {}
        if cls:
            dir_to_check = {'User': User, 'State':State, 'City':City, 'Amenity':City, 'Place': Place, 'Review':Review}
            cls = dir_to_check[cls]

            result = self.__session.query(cls).all()

            for element in result:
                key = element.__class__.__name__ + '.' + element.id
                dictionary_to_return[key] = element
        else:
            every_type = [User, State, City, Amenity, Place, Review]

            for every_class in every_type:
                query = self.__session.query(every_class).all()
                for element_no_cls in query:
                    key = element_no_cls.__class__.__name__ + '.' + element_no_cls.id
                    dictionary_to_return[key] = element_no_cls

        return dictionary_to_return

    def new(self, obj):
        '''add the object to the current database session '''
        self.__session.add(obj)
        self.__session.commit()

    def save(self):
        ''' commit all changes of the current database session '''
        self.__session.commit()

    def delete(self, obj=None):
        '''delete from the current database session '''
        if obj:
            self.__session.delete(obj)
            self.__session.commit()

    def reload(self):
        '''create all tables in the database (feature of SQLAlchemy) '''
        Base.metadata.create_all(bind=self.__engine)
        session_factory =  sessionmaker(bind=self.__engine, expire_on_commit=False, autoflush=False)
        self.__scoop = scoped_session(session_factory)
        self.__session = self.__scoop()
