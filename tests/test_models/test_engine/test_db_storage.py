#!/usr/bin/python3
"""Defines unittests for models/engine/db_storage.py."""
import pep8
import unittest
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm.session import Session
from os import getenv


class TestDBStorage(unittest.TestCase):
    """Unittests for testing the DBStorage class."""

    @classmethod
    def setUpClass(cls):
        """DBStorage testing setup."""
        if type(models.storage) == DBStorage:
            cls.storage = DBStorage()

    @classmethod
    def tearDownClass(cls):
        """DBStorage testing teardown."""
        if type(models.storage) == DBStorage:
            cls.storage._DBStorage__session.close()
            del cls.storage

    def test_pep8(self):
        """Test pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(['models/engine/db_storage.py'])
        self.assertEqual(p.total_errors, 0, "fix pep8")

    def test_docstrings(self):
        """Check for docstrings."""
        self.assertIsNotNone(DBStorage.__doc__)
        self.assertIsNotNone(DBStorage.__init__.__doc__)
        self.assertIsNotNone(DBStorage.all.__doc__)
        self.assertIsNotNone(DBStorage.new.__doc__)
        self.assertIsNotNone(DBStorage.save.__doc__)
        self.assertIsNotNone(DBStorage.delete.__doc__)
        self.assertIsNotNone(DBStorage.reload.__doc__)

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

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_init(self):
        """Test initialization."""
        self.assertTrue(isinstance(self.storage, DBStorage))

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_all(self):
        """Test default all method."""
        obj = self.storage.all()
        self.assertEqual(type(obj), dict)

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_all_cls(self):
        """Test all method with specified cls."""
        obj = self.storage.all(DBStorage)
        self.assertEqual(type(obj), dict)

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_new(self):
        """Test new method."""
        obj = self.storage.new(None)
        self.assertIsNone(obj)

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_save(self):
        """Test save method."""
        obj = self.storage.save()
        self.assertIsNone(obj)

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_delete(self):
        """Test delete method."""
        obj = self.storage.delete(None)
        self.assertIsNone(obj)

    @unittest.skipIf(type(models.storage) == FileStorage,
                     "Testing FileStorage")
    def test_reload(self):
        """Test reload method."""
        obj = self.storage.reload()
        self.assertIsNone(obj)


if __name__ == "__main__":
    unittest.main()
