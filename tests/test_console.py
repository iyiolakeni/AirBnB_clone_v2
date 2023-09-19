#!/usr/bin/python3
"""Defines unittests for console.py."""
import os
import pep8
import unittest
from unittest.mock import patch
from io import StringIO
from console import HBNBCommand
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage
from models import storage


class TestHBNBCommand(unittest.TestCase):
    """Unittests for testing the HBNB command interpreter."""

    @classmethod
    def setUpClass(cls):
        """HBNBCommand testing setup.

        Temporarily rename any existing file.json.
        Reset FileStorage objects dictionary.
        Create an instance of the command interpreter.
        """
        cls.HBNB = HBNBCommand()
        cls.storage_type = type(storage)

    @classmethod
    def tearDownClass(cls):
        """HBNBCommand testing teardown.

        Restore original file.json.
        Delete the test HBNBCommand instance.
        """
        del cls.HBNB
        if cls.storage_type == DBStorage:
            storage._DBStorage__session.close()

    def setUp(self):
        """Reset FileStorage objects dictionary."""
        FileStorage._FileStorage__objects = {}

    def tearDown(self):
        """Delete any created file.json."""
        try:
            os.remove("file.json")
        except IOError:
            pass

    def test_pep8(self):
        """Test Pep8 styling."""
        style = pep8.StyleGuide(quiet=True)
        p = style.check_files(["console.py"])
        self.assertEqual(p.total_errors, 0, "fix Pep8")


if __name__ == "__main__":
    unittest.main()
