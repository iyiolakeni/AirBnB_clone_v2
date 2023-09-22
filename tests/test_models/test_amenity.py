#!/usr/bin/python3
"""Defines unittests for models/amenity.py."""
import os
import pep8
import unittest
from datetime import datetime
from models.amenity import Amenity
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.exc import OperationalError

class TestAmenity(unittest.TestCase):
    """Unittests for testing the Amenity class."""

    @classmethod
    def setUpClass(cls):
        """Amenity testing setup."""
        cls.storage_type = os.environ.get('HBNB_TYPE_STORAGE')
        if cls.storage_type == 'db':
            cls.storage = DBStorage()
        else:
            cls.storage = FileStorage()
        cls.storage.reload()
        cls.amenity = Amenity(name="The Andrew Lindburg treatment")

    @classmethod
    def tearDownClass(cls):
        """Amenity testing teardown."""
        del cls.amenity
        del cls.storage

    def test_pep8(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/amenity.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(Amenity.__doc__)

    def test_attributes(self):
        """Check for attributes."""
        us = Amenity(email="a", password="a")
        self.assertEqual(str, type(us.id))
        self.assertEqual(datetime, type(us.created_at))
        self.assertEqual(datetime, type(us.updated_at))
        self.assertTrue(hasattr(us, "__tablename__"))
        self.assertTrue(hasattr(us, "name"))
        self.assertTrue(hasattr(us, "place_amenities"))

    def test_email_not_nullable(self):
        """Test that email attribute is non-nullable."""
        if self.storage_type == 'db':
            with self.assertRaises(OperationalError):
                self.storage.new(Amenity(password="a"))
                self.storage.save()
            with self.assertRaises(OperationalError):
                self.storage.new(Amenity(email="a"))
                self.storage.save()

    def test_is_subclass(self):
        """Check that Amenity is a subclass of BaseModel."""
        self.assertTrue(issubclass(Amenity, BaseModel))

    def test_init(self):
        """Test initialization."""
        self.assertIsInstance(self.amenity, Amenity)

    def test_two_models_are_unique(self):
        """Test that different Amenity instances are unique."""
        us = Amenity(email="a", password="a")
        self.assertNotEqual(self.amenity.id, us.id)
        self.assertLess(self.amenity.created_at, us.created_at)
        self.assertLess(self.amenity.updated_at, us.updated_at)

    def test_init_args_kwargs(self):
        """Test initialization with args and kwargs."""
        dt = datetime.utcnow()
        st = Amenity("1", id="5", created_at=dt.isoformat())
        self.assertEqual(st.id, "5")
        self.assertEqual(st.created_at, dt)

    def test_str(self):
        """Test __str__ representation."""
        s = str(self.amenity)
        self.assertIn("[Amenity] ({})".format(self.amenity.id), s)
        self.assertIn("'id': '{}'".format(self.amenity.id), s)
        self.assertIn("'created_at': {}".format(repr(self.amenity.created_at)), s)
        self.assertIn("'updated_at': {}".format(repr(self.amenity.updated_at)), s)
        self.assertIn("'name': '{}'".format(self.amenity.name), s)

    def test_save(self):
        """Test save method."""
        old_updated_at = self.amenity.updated_at
        self.amenity.save()
        new_updated_at = self.amenity.updated_at
        if self.storage_type == 'db':
            self.assertNotEqual(old_updated_at, new_updated_at)
        else:
            self.assertEqual(old_updated_at, new_updated_at)

    def test_to_dict(self):
        """Test to_dict method."""
        amenity_dict = self.amenity.to_dict()
        self.assertEqual(dict, type(amenity_dict))
        self.assertEqual(self.amenity.id, amenity_dict["id"])
        self.assertEqual("Amenity", amenity_dict["__class__"])
        self.assertEqual(self.amenity.created_at.isoformat(), amenity_dict["created_at"])
        self.assertEqual(self.amenity.updated_at.isoformat(), amenity_dict["updated_at"])
        self.assertEqual(self.amenity.name, amenity_dict["name"])

if __name__ == "__main__":
    unittest.main()
