#!/usr/bin/python3
"""Defines unittest for base_model.py """
import unittest
from datetime import datetime
from models.base_model import BaseModel
from unittest.mock import patch
import uuid


class TestBaseModel(unittest.TestCase):
    def test_instance_creation(self):
        """Test if an instance of BaseModel is created properly"""
        model = BaseModel()
        self.assertIsInstance(model, BaseModel)
        self.assertIsInstance(model.id, str)
        self.assertIsInstance(model.created_at, datetime)
        self.assertIsInstance(model.updated_at, datetime)

    def test_instance_creation_with_id(self):
        """Test if an instance of BaseModel is created with a specified ID"""
        model = BaseModel(id="test_id")
        self.assertEqual(model.id, "test_id")

    def test_instance_creation_with_kwargs(self):
        """Test if an instance of BaseModel is created properly with kwargs"""
        kwargs = {
            "id": "test_id",
            "created_at": datetime(2022, 1, 1),
            "updated_at": datetime(2022, 2, 2),
            "name": "test_name",
        }
        model = BaseModel(**kwargs)
        self.assertEqual(model.id, "test_id")
        self.assertEqual(model.created_at, datetime(2022, 1, 1))
        self.assertEqual(model.updated_at, datetime(2022, 2, 2))
        self.assertEqual(model.name, "test_name")

    @patch('models.storage.new')
    def test_save(self, mock_new):
        """Test the save method of BaseModel"""
        model = BaseModel()
        model.save()
        self.assertIsInstance(model.updated_at, datetime)
        mock_new.assert_called_once()

    def test_to_dict(self):
        """Test the to_dict method of BaseModel"""
        model = BaseModel(id="test_id", created_at=datetime(2022, 1, 1))
        model_dict = model.to_dict()
        expected_dict = {
            'id': 'test_id',
            'created_at': '2022-01-01T00:00:00',
            'updated_at': model.updated_at.isoformat(),
            '__class__': 'BaseModel'
        }
        self.assertEqual(model_dict, expected_dict)

    @patch('models.storage.delete')
    def test_delete(self, mock_delete):
        """Test the delete method of BaseModel"""
        model = BaseModel()
        model.delete()
        mock_delete.assert_called_once_with(model)


if __name__ == "__main__":
    unittest.main()
