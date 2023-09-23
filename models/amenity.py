#!/usr/bin/python3
"""Defines the Amenity class."""
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from models.base_model import BaseModel
from models.base_model import Base
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class Amenity(BaseModel, Base):
    """Represents an Amenity for a MySQL database.

    Inherits from SQLAlchemy Base and links to the MySQL table amenities.

    Attributes:
        __tablename__ (str): The name of the MySQL table to store Amenities.
        name (sqlalchemy String): The amenity name.
        place_amenities (sqlalchemy relationship): Place-Amenity relationship.
    """
    __tablename__ = 'amenities'
    
    name = Column(String(128), nullable=False)
    
    place_amenities = Table(
        "place_amenity", Base.metadata,
        Column("place_id", String(60), ForeignKey("places.id"),
               primary_key=True, nullable=False),
        Column("amenity_id", String(60), ForeignKey("amenities.id"),
               primary_key=True, nullable=False)
    )
