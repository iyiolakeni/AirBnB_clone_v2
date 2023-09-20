#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from models.base_model import BaseModel
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""

    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage
        or filtered by class"""
        if cls is None:
            return self.__objects
        filtered_objects = {}
        for key, obj in self.__objects.items():
            if obj.__class__ == cls:
                filtered_objects[key] = obj
        return filtered_objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        key = obj.__class__.__name__ + '.' + obj.id
        self.__objects[key] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(self.__file_path, 'w') as f:
            serialized_objects = {key: obj.to_dict()
                                  for key, obj in self.__objects()}
            json.dump(serialized_objects, f)

    def reload(self):
        """Loads storage dictionary from file"""
        try:
            with open(self.__file_path, 'r') as f:
                serialized_objects = json.load(f)
                for key, serialized_obj in serialized_objects.items():
                    class_name = serialized_obj['__class__']
                    if class_name in classes:
                        obj = classes[class_name](**serialized_obj)
                        self.__objects[key] = obj
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Deletes an object from storage if it exists"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """Call the reload method."""
        self.reload()
