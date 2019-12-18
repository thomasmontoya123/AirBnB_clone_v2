#!/usr/bin/python3
"""This is the city class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from os import environ

class City(BaseModel, Base):
    """This is the class for City
    Attributes:
        state_id: The state id
        name: input name
    """
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
    places = relationship("Place", backref="cities", cascade="all, delete")

    if environ['HBNB_TYPE_STORAGE'] != 'db':
        @property
        def cities(self):
            '''FileStorage relationship between State and City '''
            cities = storage.all(City)
            cities_relation = []

            for city in cities.values():
                if city.state_id == self.id:
                    cities_relation = cities_relation.append(city)
            return cities_relation
