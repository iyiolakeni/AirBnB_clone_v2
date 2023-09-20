#!/usr/bin/python3
""" Defines the Amenity class for HBNB project """
from models.base_model import BaseModel
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.orm import relationship
import os

class Amenity(BaseModel, Base):
    """Representation of Amenity """
    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        from models.base_model import Base
        __tablename__ = 'amenities'
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place", secondary="place_amenity",
                                       viewonly=False)
    else:
        name = ""

    __table_args__ = {'extend_existing': True}
