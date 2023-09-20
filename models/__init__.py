#!/usr/bin/python3
"""This module instantiates an object of class FileStorage or DBStorage"""
from os import getenv

# Check the value of HBNB_TYPE_STORAGE environment variable
if getenv("HBNB_TYPE_STORAGE") ==  "db":
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

# Load data from storage (either FileStorage or DBStorage)
storage.reload()
