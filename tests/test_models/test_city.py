#!/usr/bin/python3
"""Defines unittests for models/place.py."""
import os
import pep8
import unittest
from datetime import datetime
from models.base_model import BaseModel
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from models.amenity import Amenity
from models.state import State
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker


class TestPlace(unittest.TestCase):
    """Unittests for testing the Place class."""

    @classmethod
    def setUpClass(cls):
        """Place testing setup.

        Temporarily renames any existing file.json.
        Resets FileStorage objects dictionary.
        Creates FileStorage, DBStorage, and Place instances for testing.
        """
        try:
            os.rename("file.json", "tmp")
        except IOError:
            pass
        FileStorage._FileStorage__objects = {}
        cls.state = State(name="California")
        cls.city = City(name="San Francisco", state_id=cls.state.id)
        cls.user = User(email="poppy@holberton.com", password="betty98")
        cls.place = Place(city_id=cls.city.id, user_id=cls.user.id, name="Betty")
        cls.review = Review(text="stellar", place_id=cls.place.id, user_id=cls.user.id)
        cls.amenity = Amenity(name="water", place=cls.place.id)
        cls.filestorage = FileStorage()

        if type(models.storage) == DBStorage:
            cls.dbstorage = DBStorage()
            Session = sessionmaker(bind=cls.dbstorage._DBStorage__engine)
            cls.dbstorage._DBStorage__session = Session()

    @classmethod
    def tearDownClass(cls):
        """Place testing teardown.

        Restore the original file.json.
        Delete test instances.
        """
        try:
            os.remove("file.json")
        except IOError:
            pass
        try:
            os.rename("tmp", "file.json")
        except IOError:
            pass
        del cls.state
        del cls.city
        del cls.user
        del cls.place
        del cls.review
        del cls.amenity
        del cls.filestorage
        if type(models.storage) == DBStorage:
            cls.dbstorage._DBStorage__session.close()
            del cls.dbstorage

    def test_pep8(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["models/place.py"])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(Place.__doc__)

    def test_attributes(self):
        """Check for attributes."""
        pl = Place()
        self.assertEqual(str, type(pl.id))
        self.assertEqual(datetime, type(pl.created_at))
        self.assertEqual(datetime, type(pl.updated_at))
        self.assertTrue(hasattr(pl, "__tablename__"))
        self.assertTrue(hasattr(pl, "city_id"))
        self.assertTrue(hasattr(pl, "name"))
        self.assertTrue(hasattr(pl, "description"))
        self.assertTrue(hasattr(pl, "number_rooms"))
        self.assertTrue(hasattr(pl, "number_bathrooms"))
        self.assertTrue(hasattr(pl, "max_guest"))
        self.assertTrue(hasattr(pl, "price_by_night"))
        self.assertTrue(hasattr(pl, "latitude"))
        self.assertTrue(hasattr(pl, "longitude"))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_nullable_attributes(self):
        """Test that relevant attributes are non-nullable."""
        with self.assertRaises(OperationalError):
            Place(user_id=self.user.id, name="Betty")
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            Place(city_id=self.city.id, name="Betty")
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()
        with self.assertRaises(OperationalError):
            Place(city_id=self.city.id, user_id=self.user.id)
            self.dbstorage._DBStorage__session.commit()
        self.dbstorage._DBStorage__session.rollback()

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_reviews_filestorage(self):
        """Test reviews attribute."""
        key = "{}.{}".format(type(self.review).__name__, self.review.id)
        self.filestorage._FileStorage__objects[key] = self.review
        reviews = self.place.reviews
        self.assertTrue(list, type(reviews))
        self.assertIn(self.review, reviews)

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_amenities(self):
        """Test amenities attribute."""
        key = "{}.{}".format(type(self.amenity).__name__, self.amenity.id)
        self.filestorage._FileStorage__objects[key] = self.amenity
        self.place.amenities = self.amenity
        amenities = self.place.amenities
        self.assertTrue(list, type(amenities))
        self.assertIn(self.amenity, amenities)

    def test_is_subclass(self):
        """Check that Place is a subclass of BaseModel."""
        self.assertTrue(issubclass(Place, BaseModel))

    def test_init(self):
        """Test initialization."""
        self.assertIsInstance(self.place, Place)

    def test_two_models_are_unique(self):
        """Test that different Place instances are unique."""
        pl = Place()
        self.assertNotEqual(self.place.id, pl.id)
        self.assertLess(self.place.created_at, pl.created_at)
        self.assertLess(self.place.updated_at, pl.updated_at)

    def test_init_args_kwargs(self):
        """Test initialization with args and kwargs."""
        dt = datetime.utcnow()
        pl = Place("1", id="5", created_at=dt.isoformat())
        self.assertEqual(pl.id, "5")
        self.assertEqual(pl.created_at, dt)

    def test_str(self):
        """Test __str__ representation."""
        s = self.place.__str__()
        self.assertIn("[Place] ({})".format(self.place.id), s)
        self.assertIn("'id': '{}'".format(self.place.id), s)
        self.assertIn("'created_at': {}".format(repr(self.place.created_at)), s)
        self.assertIn("'updated_at': {}".format(repr(self.place.updated_at)), s)
        self.assertIn("'city_id': '{}'".format(self.place.city_id), s)
        self.assertIn("'user_id': '{}'".format(self.place.user_id), s)
        self.assertIn("'name': '{}'".format(self.place.name), s)

    @unittest.skipIf(type(models.storage) == DBStorage,
                     "Testing DBStorage")
    def test_save_filestorage(self):
        """Test save method with FileStorage."""
        old = self.place.updated_at
        self.place.save()
        self.assertLess(old, self.place.updated_at)
        with open("file.json", "r") as f:
            self.assertIn("Place." + self.place.id, f.read())

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_save_dbstorage(self):
        """Test save method with DBStorage."""
        old = self.place.updated_at
        self.state.save()
        self.city.save()
        self.user.save()
        self.place.save()
        self.assertLess(old, self.place.updated_at)
        db = MySQLdb.connect(user="hbnb_test", passwd="hbnb_test_pwd", db="hbnb_test_db")
        cursor = db.cursor()
        cursor.execute("SELECT * FROM `places` WHERE BINARY name = '{}'".
                       format(self.place.name))
        query = cursor.fetchall()
        self.assertEqual(1, len(query))
        self.assertEqual(self.place.id, query[0][0])
        cursor.close()

    def test_to_dict(self):
        """Test to_dict method."""
        place_dict = self.place.to_dict()
        self.assertEqual(dict, type(place_dict))
        self.assertEqual(self.place.id, place_dict["id"])
        self.assertEqual("Place", place_dict["__class__"])
        self.assertEqual(self.place.created_at.isoformat(), place_dict["created_at"])
        self.assertEqual(self.place.updated_at.isoformat(), place_dict["updated_at"])
        self.assertEqual(self.place.city_id, place_dict["city_id"])
        self.assertEqual(self.place.user_id, place_dict["user_id"])
        self.assertEqual(self.place.name, place_dict["name"])


if __name__ == "__main__":
    unittest.main()
