#!/usr/bin/python3
"""Defines unittests for models/city.py."""
import os
import pep8
import unittest
from datetime import datetime
from models.city import City
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.exc import OperationalError
from models.base_model import BaseModel

class TestCity(unittest.TestCase):
    """Unittests for testing the City class."""

    @classmethod
    def setUpClass(cls):
        """City testing setup."""
        cls.storage_type = os.environ.get('HBNB_TYPE_STORAGE')
        if cls.storage_type == 'db':
            cls.storage = DBStorage()
        else:
            cls.storage = FileStorage()
        cls.storage.reload()
        cls.city = City(name="San Francisco")

    @classmethod
    def tearDownClass(cls):
        """City testing teardown."""
        del cls.city
        del cls.storage

    def test_pep8(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/city.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(City.__doc__)

    def test_attributes(self):
        """Check for attributes."""
        self.assertEqual(str, type(self.city.id))
        self.assertEqual(datetime, type(self.city.created_at))
        self.assertEqual(datetime, type(self.city.updated_at))
        self.assertTrue(hasattr(self.city, "__tablename__"))
        self.assertTrue(hasattr(self.city, "name"))
        self.assertTrue(hasattr(self.city, "state_id"))

    @unittest.skipIf(os.getenv("HBNB_ENV") is not None, "Testing DBStorage")
    def test_nullable_attributes(self):
        """Check that relevant DBStorage attributes are non-nullable."""
        with self.assertRaises(OperationalError):
            self.storage.new(City())
            self.storage.save()
        with self.assertRaises(OperationalError):
            self.storage.new(City(state_id="state_id"))
            self.storage.save()

    def test_is_subclass(self):
        """Check that City is a subclass of BaseModel."""
        self.assertTrue(issubclass(City, BaseModel))

    def test_init(self):
        """Test initialization."""
        self.assertIsInstance(self.city, City)

    def test_init_args_kwargs(self):
        """Test initialization with args and kwargs."""
        dt = datetime.utcnow()
        ct = City("1", id="5", created_at=dt.isoformat())
        self.assertEqual(ct.id, "5")
        self.assertEqual(ct.created_at, dt)

    def test_str(self):
        """Test __str__ representation."""
        s = str(self.city)
        self.assertIn("[City] ({})".format(self.city.id), s)
        self.assertIn("'id': '{}'".format(self.city.id), s)
        self.assertIn("'created_at': {}".format(repr(self.city.created_at)), s)
        self.assertIn("'updated_at': {}".format(repr(self.city.updated_at)), s)
        self.assertIn("'name': '{}'".format(self.city.name), s)
        self.assertIn("'state_id': '{}'".format(self.city.state_id), s)

    def test_save(self):
        """Test save method."""
        old_updated_at = self.city.updated_at
        self.city.save()
        new_updated_at = self.city.updated_at
        if self.storage_type == 'db':
            self.assertNotEqual(old_updated_at, new_updated_at)
        else:
            self.assertEqual(old_updated_at, new_updated_at)

    def test_to_dict(self):
        """Test to_dict method."""
        city_dict = self.city.to_dict()
        self.assertEqual(dict, type(city_dict))
        self.assertEqual(self.city.id, city_dict["id"])
        self.assertEqual("City", city_dict["__class__"])
        self.assertEqual(self.city.created_at.isoformat(), city_dict["created_at"])
        self.assertEqual(self.city.updated_at.isoformat(), city_dict["updated_at"])
        self.assertEqual(self.city.name, city_dict["name"])
        self.assertEqual(self.city.state_id, city_dict["state_id"])

if __name__ == "__main__":
    unittest.main()
