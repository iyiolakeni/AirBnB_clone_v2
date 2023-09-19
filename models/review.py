#!/usr/bin/python3
""" Define Review class module """
from models.base_model import Base
from os import getenv
from models.base_model import BaseModel
from sqlalchemy import Column, String
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Review(BaseModel, ):
    """ Representation for Review class """
    if getenv('HBNB_TYPE_STORAGE') != 'db':
        text = ""
        place_id = ""
        user_id = ""
    else:
        __tablename__ = "reviews"
        text = Column(String(1024), nullable=False)
        place_id = Column(String(60), ForeignKey("places.id"),
                          nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"),
                         nullable=False)
