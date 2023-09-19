#!/usr/bin/python3
""" State Module for HBNB project """
import os
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship

class State(BaseModel):
    """ State class """
    __tablename__ = 'states'  # Table name is 'states'
    name = Column(String(128), nullable=False)  # Column for state name

    # Define the relationship with City for DBStorage
    if os.environ.get('HBNB_TYPE_STORAGE') == 'db':
        cities = relationship("City", backref="state", cascade="all, delete-orphan")
    else:
        @property
        def cities(self):
            """Getter attribute to return a list of City instances with state_id equal to State.id"""
            from models import storage
            city_list = []
            for city in storage.all("City").values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
