#!/usr/bin/python3
""" """
from tests.test_models.test_base_model import TestBaseModel
from models.state import State
import unittest
from models.state import State
from models.city import City
from models.base_model import BaseModel
from os import getenv
from unittest.mock import patch
from io import StringIO


class TestState(unittest.TestCase):
    def test_attributes(self):
        state = State()
        self.assertTrue(hasattr(state, "name"))
        self.assertTrue(hasattr(state, "cities"))
        self.assertTrue(hasattr(state, "__tablename__"))

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != "db", "Not using DBStorage")
    def test_relationship(self):
        state = State()
        self.assertIsInstance(state.cities, list)
        self.assertEqual(state.cities, [])

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == "db", "Using DBStorage")
    def test_cities_property(self):
        state = State()
        city1 = City(state_id=state.id)
        city2 = City(state_id=state.id)
        BaseModel._BaseModel__objects = {}
        BaseModel._BaseModel__objects["City." + city1.id] = city1
        BaseModel._BaseModel__objects["City." + city2.id] = city2
        cities = state.cities
        self.assertIsInstance(cities, list)
        self.assertEqual(len(cities), 2)
        self.assertIn(city1, cities)
        self.assertIn(city2, cities)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == "db", "Using DBStorage")
    def test_cities_property_no_match(self):
        state = State()
        city = City(state_id="non_matching_id")
        BaseModel._BaseModel__objects = {}
        BaseModel._BaseModel__objects["City." + city.id] = city
        cities = state.cities
        self.assertIsInstance(cities, list)
        self.assertEqual(len(cities), 0)

    def test_to_dict(self):
        state = State()
        state_dict = state.to_dict()
        self.assertEqual(state_dict["name"], "")
        self.assertEqual(state_dict["cities"], [])
        self.assertEqual(state_dict["__class__"], "State")
        self.assertIn("id", state_dict)
        self.assertIn("created_at", state_dict)
        self.assertIn("updated_at", state_dict)

    def test_str(self):
        state = State()
        state_str = str(state)
        self.assertIn("[State]", state_str)
        self.assertIn(str(state.id), state_str)
        self.assertIn(str(state.__dict__), state_str)

    def test_str_no_id(self):
        state = State()
        del state.id
        state_str = str(state)
        self.assertIn("[State]", state_str)
        self.assertIn("None", state_str)
        self.assertIn(str(state.__dict__), state_str)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == "db", "Using DBStorage")
    def test_delete(self):
        state = State()
        city = City(state_id=state.id)
        BaseModel._BaseModel__objects = {}
        BaseModel._BaseModel__objects["City." + city.id] = city
        state.delete()
        self.assertNotIn(city, BaseModel._BaseModel__objects.values())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != "db", "Not using DBStorage")
    def test_delete(self):
        state = State()
        city = City(state_id=state.id)
        BaseModel._BaseModel__objects = {}
        BaseModel._BaseModel__objects["City." + city.id] = city
        state.delete()
        self.assertEqual(city.state_id, None)

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != "db", "Not using DBStorage")
    def test_delete_no_match(self):
        state = State()
        city = City(state_id="non_matching_id")
        BaseModel._BaseModel__objects = {}
        BaseModel._BaseModel__objects["City." + city.id] = city
        state.delete()
        self.assertIn(city, BaseModel._BaseModel__objects.values())

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != "db", "Not using DBStorage")
    def test_delete_no_match(self):
        state = State()
        city = City(state_id="non_matching_id")
        BaseModel._BaseModel__objects = {}
        BaseModel._BaseModel__objects["City." + city.id] = city
        state.delete()
        self.assertIn(city, BaseModel._BaseModel__objects.values())

    def test_reload(self):
        with patch("models.storage.reload") as mock_reload:
            state = State()
            state.reload()
            mock_reload.assert_called_once()

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == "db", "Using DBStorage")
    def test_reload(self):
        state = State()
        with patch("models.storage.reload") as mock_reload:
            state.reload()
            mock_reload.assert_not_called()

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == "db", "Using DBStorage")
    def test_save(self):
        state = State()
        with patch("models.storage.save") as mock_save:
            state.save()
            mock_save.assert_called_once()

    def test_save_no_db(self):
        state = State()
        with patch("models.storage.save") as mock_save:
            state.save()
            mock_save.assert_not_called()

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == "db", "Using DBStorage")
    def test_new(self):
        state = State()
        with patch("models.storage.new") as mock_new:
            state.new()
            mock_new.assert_called_once()

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != "db", "Not using DBStorage")
    def test_new(self):
        state = State()
        with patch("models.storage.new") as mock_new:
            state.new()
            mock_new.assert_not_called()

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") == "db", "Using DBStorage")
    def test_new_with_object(self):
        state = State()
        city = City()
        with patch("models.storage.new") as mock_new:
            state.new(city)
            mock_new.assert_called_once()

    @unittest.skipIf(getenv("HBNB_TYPE_STORAGE") != "db", "Not using DBStorage")
    def test_new_with_object(self):
        state = State()
        city = City()
        with patch("models.storage.new") as mock_new:
            state.new(city)
            mock_new.assert_not_called()

if __name__ == "__main__":
    unittest.main()
