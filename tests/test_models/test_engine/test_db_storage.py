import unittest
import os
from models.base_model import BaseModel
from models.state import State
from models.city import City
from models import storage
from models.engine.db_storage import DBStorage

class TestDBStorage(unittest.TestCase):
    """Unit tests for DBStorage class"""

    @classmethod
    def setUpClass(cls):
        """Set up the test database"""
        os.environ['HBNB_MYSQL_USER'] = 'your_test_user'
        os.environ['HBNB_MYSQL_PWD'] = 'your_test_password'
        os.environ['HBNB_MYSQL_HOST'] = 'localhost'
        os.environ['HBNB_MYSQL_DB'] = 'your_test_db'
        os.environ['HBNB_ENV'] = 'test'

    def setUp(self):
        """Set up the test environment"""
        self.db = DBStorage()
        self.db.reload()

    def tearDown(self):
        """Clean up after each test"""
        self.db.close()

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

    def test_delete(self):
        """Test deleting objects from the database"""
        state = State(name="California")
        city = City(name="San Francisco", state_id=state.id)

        # Save objects to the database
        self.db.new(state)
        self.db.new(city)
        self.db.save()

        # Delete the city object and save
        self.db.delete(city)
        self.db.save()

        # Retrieve the city object from the database
        retrieved_city = self.db.all(City).values()

        self.assertFalse(city in retrieved_city)

if __name__ == '__main__':
    unittest.main()
