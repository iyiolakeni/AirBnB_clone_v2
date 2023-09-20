#!/usr/bin/python3
"""Defines console command unittests """
import os
import unittest
import models
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

    def test_emptyline(self):
        """Test empty line input."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("\n")
            self.assertEqual("", f.getvalue())

    def test_quit(self):
        """Test quit command input."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.HBNB.onecmd("quit")
            self.assertEqual("", f.getvalue())

    def test_EOF(self):
        """Test that EOF quits."""
        with patch("sys.stdout", new=StringIO()) as f:
            self.assertTrue(self.HBNB.onecmd("EOF"))

    @unittest.skipIf(type(models.storage) == DBStorage, "Test DBStorage")
    def test_create(self):
        """Test create command."""
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("create BaseModel")
            base = cons.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("create User")
            user = cons.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("create State")
            state = cons.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("create Place")
            place = cons.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("create City")
            city = cons.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("create Review")
            review = cons.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("create Amenity")
            amenity = cons.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("all BaseModel")
            self.assertIn(base, cons.getvalue())
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("all User")
            self.assertIn(user, cons.getvalue())
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("all State")
            self.assertIn(state, cons.getvalue())
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("all Place")
            self.assertIn(place, cons.getvalue())
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("all City")
            self.assertIn(city, cons.getvalue())
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("all Review")
            self.assertIn(review, cons.getvalue())
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("all Amenity")
            self.assertIn(amenity, cons.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Test DBStorage")
    def test_create_args(self):
        """Test create command with args."""
        with patch("sys.stdout", new=StringIO()) as cons:
            call = ('create Place city_id="0001" name="John_Doe" '
                    'number_rooms=3 latitude=29.73 longitude=a')
            self.HBNB.onecmd(call)
            pl = cons.getvalue().strip()
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("all Place")
            output = cons.getvalue()
            self.assertIn(pl, output)
            self.assertIn("'city_id': '0001'", output)
            self.assertIn("'name': 'John Doe'", output)
            self.assertIn("'number_rooms': 3", output)
            self.assertIn("'latitude': 29.73", output)
            self.assertNotIn("'longitude'", output)

    def test_show(self):
        """Test show command."""
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("show")
            self.assertEqual(
                "** class name missing **\n", cons.getvalue())
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("show asdfsdrfs")
            self.assertEqual(
                "** class doesn't exist **\n", cons.getvalue())
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("show BaseModel")
            self.assertEqual(
                "** instance id missing **\n", cons.getvalue())
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("show BaseModel abcd-123")
            self.assertEqual(
                "** no instance found **\n", cons.getvalue())

    def test_destroy(self):
        """Test destroy command input."""
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("destroy")
            self.assertEqual(
                "** class name missing **\n", cons.getvalue())
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("destroy Galaxy")
            self.assertEqual(
                "** class doesn't exist **\n", cons.getvalue())
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("destroy User")
            self.assertEqual(
                "** instance id missing **\n", cons.getvalue())
        with patch('sys.stdout', new=StringIO()) as cons:
            self.HBNB.onecmd("destroy BaseModel 12345")
            self.assertEqual(
                "** no instance found **\n", cons.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Test DBStorage")
    def test_all(self):
        """Test all command input."""
        with patch('sys.stdout', new=StringIO()) as cons:
            self.HBNB.onecmd("all afnknjkkm")
            self.assertEqual("** class doesn't exist **\n", cons.getvalue())
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("all State")
            self.assertEqual("[]\n", cons.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Test DBStorage")
    def test_update(self):
        """Test update command input."""
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("update")
            self.assertEqual(
                "** class name missing **\n", cons.getvalue())
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("update jsljhvf")
            self.assertEqual(
                "** class doesn't exist **\n", cons.getvalue())
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("update User")
            self.assertEqual(
                "** instance id missing **\n", cons.getvalue())
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("update User 12345")
            self.assertEqual(
                "** no instance found **\n", cons.getvalue())
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("all User")
            obj = cons.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("update User " + my_id)
            self.assertEqual(
                "** attribute name missing **\n", cons.getvalue())
        with patch("sys.stdout", new=StringIO()) as cons:
            self.HBNB.onecmd("update User " + my_id + " Name")
            self.assertEqual(
                "** value missing **\n", cons.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Testing DBStorage")
    def test_count(self):
        """Test count command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("sjdsljd.count()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("State.count()")
            self.assertEqual("0\n", f.getvalue())

    @unittest.skipIf(type(models.storage) == DBStorage, "Test DBStorage")
    def test_update(self):
        """Test alternate destroy command inpout"""
        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("slhbvfjj.update()")
            self.assertEqual(
                "** class doesn't exist **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("User.update(56789)")
            self.assertEqual(
                "** no instance found **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("create User")
        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("all User")
            obj = f.getvalue()
        my_id = obj[obj.find('(')+1:obj.find(')')]
        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("User.update(" + my_id + ")")
            self.assertEqual(
                "** attribute name missing **\n", f.getvalue())
        with patch('sys.stdout', new=StringIO()) as f:
            self.HBNB.onecmd("User.update(" + my_id + ", name)")
            self.assertEqual(
                "** value missing **\n", f.getvalue())


if __name__ == "__main__":
    unittest.main()
