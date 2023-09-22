#!/usr/bin/python3
"""Defines the City class."""
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel
from models.base_model import Base

class City(BaseModel, Base):
    """Represents a City for a MySQL database.

    Inherits from SQLAlchemy Base and links to the MySQL table cities.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store Cities.
        name (sqlalchemy String): The city name.
        state_id (sqlalchemy String): The state id.
        places (sqlalchemy relationship): Relationship to Place class.
    """
    __tablename__ = "cities"
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    places = relationship("Place", backref="cities", cascade="delete")
