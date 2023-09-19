#!/usr/bin/python3
""" Define the Place Module """
import models
from os import getenv
from models.amenity import Amenity
from models.review import Review
from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import Table
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


place_table = Table("place_amenity", Base.metadata,
                    Column("place_id",
                           String(60),
                           ForeignKey("places.id"),
                           primary_key=True, nullable=False),
                    Column("amenity_id",
                           String(60),
                           ForeignKey("amenities.id"),
                           primary_key=True, nullable=False))


class Place(BaseModel):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60),
                     ForeignKey('cities.id'),
                     nullable=False)
    user_id = Column(String(60),
                     ForeignKey('users.id'),
                     nullable=False)
    name = Column(String(128),
                  nullable=False)
    description = Column(String(1024),
                         nullable=True)
    number_rooms = Column(Integer,
                          nullable=False,
                          default=0)
    number_bathrooms = Column(Integer,
                              nullable=False,
                              default=0)
    max_guest = Column(Integer, nullable=False,
                       default=0)
    price_by_night = Column(Integer,
                            nullable=False,
                            default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    reviews = relationship("Review", backref="place", cascade="delete")
    amenities = relationship("Amenity", secondary="place_amenity",
                             viewonly=False)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """Returns list of all linked Reviews."""
            value_rev = models.storage.all(Review).values()
            review_list = []
            for review in list(value_rev):
                if review.place_id == self.id:
                    review_list.append(review)
            return review_list

        @property
        def amenities(self):
            """Returns list of Amenities."""
            value_ame = models.storage.all(Amenity).values()
            amenity_list = []
            for amenity in list(value_ame):
                if amenity.id in self.amenity_ids:
                    amenity_list.append(amenity)
            return amenity_list

        @amenities.setter
        def amenities(self, value):
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
