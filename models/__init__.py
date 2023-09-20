#!/usr/bin/python3
"""This module instantiates an object of class FileStorage or DBStorage"""
from os import getenv
from models.engine.db_storage import DBStorage
from models.engine.file_storage import FileStorage

# Check the value of HBNB_TYPE_STORAGE environment variable
if getenv('HBNB_TYPE_STORAGE') == 'db':
    storage = DBStorage()
else:
    storage = FileStorage()

# Load data from storage (either FileStorage or DBStorage)
storage.reload()
