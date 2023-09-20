#!/usr/bin/python3
"""Unit tests for the Amenity class"""
import unittest
from models.amenity import Amenity
from models.base_model import BaseModel
from models.base_model import Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class TestAmenity(unittest.TestCase):
    def test_inheritance(self):
        amenity = Amenity()
        self.assertIsInstance(amenity, BaseModel)
        self.assertIsInstance(amenity, Base)

    def test_attributes(self):
        amenity = Amenity()
        self.assertTrue(hasattr(amenity, 'name'))
        self.assertIsInstance(amenity.name, str)

    def test_db_table(self):
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            self.assertEqual(Amenity.__tablename__, 'amenities')

    def test_relationship(self):
        amenity = Amenity()
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            self.assertTrue(hasattr(amenity, 'place_amenities'))
            self.assertTrue(isinstance(amenity.place_amenities, relationship))


if __name__ == '__main__':
    unittest.main()
