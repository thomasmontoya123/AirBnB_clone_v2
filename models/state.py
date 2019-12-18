#!/usr/bin/python3
"""This is the state class"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import models
from os import environ


class State(BaseModel):
    """This is the class for State
    Attributes:
        name: input name
    """
    __tablename__ = 'states'
    name = Column(String(128), nullable=False)
    cities_state = relationship("City", backref="state", cascade="all, delete")

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