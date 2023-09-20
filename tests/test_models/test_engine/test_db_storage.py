#!/usr/bin/python3
"""Defines unnittests for db_storage"""
import unittest
import MySQLdb
import os
import models
from models.base_model import Base
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session


class TestDBStorage(unittest.TestCase):
    """Unit tests for DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up the test database"""
        cls.storage = DBStorage()
        Base.metadata.create_all(cls.storage._DBStorage__engine)
        Session = sessionmaker(bind=cls.storage._DBStorage__engine)
        cls.storage._DBStorage__session = Session()
        cls.state = State(name="California")
        cls.storage._DBStorage__session.add(cls.state)
        cls.city = City(name="San_Jose", state_id=cls.state.id)
        cls.storage._DBStorage__session.add(cls.city)
        cls.user = User(email="poppy@holberton.com", password="betty")
        cls.storage._DBStorage__session.add(cls.user)
        cls.place = Place(city_id=cls.city.id, user_id=cls.user.id,
                          name="School")
        cls.storage._DBStorage__session.add(cls.place)
        cls.amenity = Amenity(name="Wifi")
        cls.storage._DBStorage__session.add(cls.amenity)
        cls.review = Review(place_id=cls.place.id, user_id=cls.user.id,
                            text="stellar")
        cls.storage._DBStorage__session.add(cls.review)
        cls.storage._DBStorage__session.commit()

    def setUp(self):
        """Set up the test environment"""
        self.db = DBStorage()
        self.db.reload()

    def tearDown(self):
        """Clean up after each test"""
        self.db.close()

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_attributes(self):
        """Check for attributes."""
        self.assertTrue(isinstance(self.storage._DBStorage__engine, Engine))
        self.assertTrue(isinstance(self.storage._DBStorage__session, Session))

    def test_methods(self):
        """Check for methods."""
        self.assertTrue(hasattr(DBStorage, "__init__"))
        self.assertTrue(hasattr(DBStorage, "all"))
        self.assertTrue(hasattr(DBStorage, "new"))
        self.assertTrue(hasattr(DBStorage, "save"))
        self.assertTrue(hasattr(DBStorage, "delete"))
        self.assertTrue(hasattr(DBStorage, "reload"))

    def test_create_and_save(self):
        """Test creating and saving objects to the database"""
        state = State(name="California")
        city = City(name="San Francisco", state_id=state.id)

        # Save objects to the database
        self.db.new(state)
        self.db.new(city)
        self.db.save()

        # Retrieve the objects from the database
        retrieved_state = self.db.all(State).values()
        retrieved_city = self.db.all(City).values()

        self.assertTrue(state in retrieved_state)
        self.assertTrue(city in retrieved_city)

    def test_save(self):
        """Test saving objects"""
        st = State(name="California")
        self.storage._DBStorage__session.add(st)
        self.storage.save()
        db = MySQLdb.connect(user="hbnb_test",
                             host="hbnb_test_host",
                             passwd="hbnb_test_pwd",
                             db="hbnb_test_db")
        curs = db.cursor()
        curs.execute("SELECT * FROM states WHERE BINARY name = 'California'")
        count = curs.fetchall()
        self.assertEqual(1, len(count))
        self.assertEqual(st.id, count[0][0])
        curs.close()

    def test_delete(self):
        """Test deleting objects from the database"""
        state = State(name="California")
        self.storage._DBStorage__session.add(state)
        self.storage._DBStorage__session.commit()
        self.storage.delete(state)
        self.assertIn(state, list(self.storage._DBStorage__session.deleted))

    def test_reload(self):
        """Test reloading database"""
        old_sess = self.storage._DBStorage__session
        self.storage.reload()
        self.assertIsInstance(self.storage._DBStorage__session, Session)
        self.assertNotEqual(old_sess, self.storage._DBStorage__session)
        self.storage._DBStorage__session.close()
        self.storage._DBStorage__session = old_sess


if __name__ == '__main__':
    unittest.main()
