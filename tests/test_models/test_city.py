#!/usr/bin/python3
import unittest
from models.city import City
from models.base_model import BaseModel
from sqlalchemy.orm import Session
from models import storage
import os

class test_City(unittest.TestCase):
    """Test the City class"""

    @classmethod
    def setUpClass(cls):
        """Set up the test class"""
        cls.city = City()
        cls.city.name = "Test City"
        cls.city.state_id = "Test State"

    @classmethod
    def tearDownClass(cls):
        """Tear down the test class"""
        del cls.city

    def test_inheritance(self):
        """Test that City inherits from BaseModel"""
        self.assertTrue(issubclass(City, BaseModel))

    def test_attributes(self):
        """Test City attributes"""
        self.assertTrue(hasattr(self.city, "name"))
        self.assertTrue(hasattr(self.city, "state_id"))

    def test_attributes_type(self):
        """Test the data types of City attributes"""
        self.assertIsInstance(self.city.name, str)
        self.assertIsInstance(self.city.state_id, str)

    def test_attributes_default(self):
        """Test default attribute values"""
        self.assertEqual(self.city.name, "")
        self.assertEqual(self.city.state_id, "")

    def test_save_method(self):
        """Test save method"""
        city_copy = self.city.to_dict()
        self.city.save()
        self.assertNotEqual(city_copy["updated_at"], self.city.updated_at)

    def test_str_method(self):
        """Test __str__ method"""
        expected_str = "[City] ({}) {}".format(self.city.id, self.city.__dict__)
        self.assertEqual(str(self.city), expected_str)

    def test_to_dict_method(self):
        """Test to_dict method"""
        city_dict = self.city.to_dict()
        self.assertEqual(city_dict["__class__"], "City")
        self.assertIsInstance(city_dict["created_at"], str)
        self.assertIsInstance(city_dict["updated_at"], str)

    def test_to_dict_method_with_args(self):
        """Test to_dict method with args"""
        city_dict = self.city.to_dict(None)
        self.assertNotIn("__class__", city_dict)

    def test_state_id_column(self):
        """Test the state_id column in the database"""
        city = City(state_id="Test State ID", name="Test City Name")
        storage.new(city)
        storage.save()
        state_id = city.state_id
        retrieved_city = storage.get(City, city.id)
        self.assertEqual(state_id, retrieved_city.state_id)

if __name__ == '__main__':
    unittest.main()
