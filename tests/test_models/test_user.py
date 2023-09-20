#!/usr/bin/python3
""" """
import unittest
import os
from models.base_model import BaseModel
from models.base_model import Base
from tests.test_models.test_base_model import TestBaseModel
from models.user import User
from models.place import Place
from sqlalchemy import Column, String


class TestUser(unittest.TestCase):

    def test_attributes(self):
        """Check if User class inherits from BaseModel and Base"""
        self.assertTrue(issubclass(User, BaseModel))
        self.assertTrue(issubclass(User, Base))

        # Create an instance of User
        user = User()

        """ Check if class attributes exist"""
        self.assertTrue(hasattr(User, '__tablename__'))
        self.assertTrue(hasattr(User, 'email'))
        self.assertTrue(hasattr(User, 'password'))
        self.assertTrue(hasattr(User, 'first_name'))
        self.assertTrue(hasattr(User, 'last_name'))

        """Check the data types of class attributes"""
        self.assertIsInstance(User.__tablename__, str)
        self.assertIsInstance(User.email.property.columns[0].type, String)
        self.assertIsInstance(User.password.property.columns[0].type, String)
        self.assertIsInstance(User.first_name.property.columns[0].type, String)
        self.assertIsInstance(User.last_name.property.columns[0].type, String)

        """ Check the nullability of attributes"""
        self.assertFalse(User.email.property.columns[0].nullable)
        self.assertFalse(User.password.property.columns[0].nullable)
        self.assertTrue(User.first_name.property.columns[0].nullable)
        self.assertTrue(User.last_name.property.columns[0].nullable)


if __name__ == '__main__':
    unittest.main()
