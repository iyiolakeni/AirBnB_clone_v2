#!/usr/bin/python3
""" """
from os import getenv
from tests.test_models.test_base_model import TestBaseModel
from models.place import Place


class test_Place(TestBaseModel):
    """ """

    def __init__(self, *args, **kwargs):
        """ Initialise test """
        super().__init__(*args, **kwargs)
        self.name = "Place"
        self.value = Place

    def test_name(self):
        """ test name"""
        new = self.value()
        self.assertEqual(type(new.name), str if
                         getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_description(self):
        """test place description """
        new = self.value()
        self.assertEqual(type(new.description), str if
                         getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_city_id(self):
        """ test place city_id"""
        new = self.value()
        self.assertEqual(type(new.city_id), str if
                         getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_user_id(self):
        """ test place user_id"""
        new = self.value()
        self.assertEqual(type(new.user_id), str if
                         getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_number_rooms(self):
        """ test place room numbers"""
        new = self.value()
        self.assertEqual(type(new.number_rooms), int if
                         getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_number_bathrooms(self):
        """ test place bathroom numbers"""
        new = self.value()
        self.assertEqual(type(new.number_bathrooms), int if
                         getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_max_guest(self):
        """ test place max_guest"""
        new = self.value()
        self.assertEqual(type(new.max_guest), int if
                         getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_price_by_night(self):
        """ testing place price by night attr"""
        new = self.value()
        self.assertEqual(type(new.price_by_night), int if
                         getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_amenity_ids(self):
        """ test amenity ids"""
        new = self.value()
        self.assertEqual(type(new.amenity_ids), list if
                         getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_latitude(self):
        """ test place latitud"""
        new = self.value()
        self.assertEqual(type(new.latitude), float if
                         getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_longitude(self):
        """ test place longitude"""
        new = self.value()
        self.assertEqual(type(new.latitude), float if
                         getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))
