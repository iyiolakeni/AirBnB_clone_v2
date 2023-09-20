#!/usr/bin/python3
""" Unittests for testing the Review class"""
from os import getenv
from tests.test_models.test_base_model import TestBaseModel
from models.review import Review


class test_review(TestBaseModel):
    """ """

    def __init__(self, *args, **kwargs):
        """ """
        super().__init__(*args, **kwargs)
        self.name = "Review"
        self.value = Review

    def test_text(self):
        """ test review text"""
        new = self.value()
        self.assertEqual(type(new.text), str if
                         getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_place_id(self):
        """ test review place_id"""
        new = self.value()
        self.assertEqual(type(new.place_id), str if
                         getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))

    def test_user_id(self):
        """ test review user_id"""
        new = self.value()
        self.assertEqual(type(new.user_id), str if
                         getenv('HBNB_TYPE_STORAGE') != 'db'
                         else type(None))
