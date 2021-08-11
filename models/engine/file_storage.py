#!/usr/bin/python3
"""
    This is the class to store objects
"""
import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review

classes = {'BaseModel': BaseModel,
           'User': User,
           'State': State,
           'City': City,
           'Amenity': Amenity,
           'Place': Place,
           'Review': Review}


class FileStorage:
    """
    Class FileStorage that serializes instances to a JSON file and
    deserializes JSON file to instances
    """
    __file_path = 'file.json'
    __objects = {}

    """------------------------------- METHODS ----------------------------"""
    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects
    def new(self, obj):
        """
        Method to sets in __objects the obj with key
        """
        key = "{}.{}".format(obj.__class__.__name__, obj.id)
        self.__objects[key] = obj

    def save(self):
        """
        Method to serialize __objects to the JSON file
        """
        save_dict = {}
        for key, value in self.__objects.items():
            save_dict[key] = value.to_dict()

        with open(self.__file_path, 'w', encoding='utf-8') as my_file:
            json.dump(save_dict, my_file)

    def reload(self):
        """
            Method to deserealizes the JSON file to __objects
        """
        try:
            with open(self.__file_path, 'r', encoding='utf-8') as my_file:
                objs = json.load(my_file)

            """for key, value in objects.items():
                if value['__class__'] == 'BaseModel':
                    FileStorage.__objects[key] = User(**value)"""
            for key in objs:
                self.__objects[key] = (classes[objs[key]["__class__"]]
                                       (**objs[key]))

        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ Deletes an object from __objects. """
        if obj:
            objDict = obj.to_dict()
            objDict = "{}.{}".format(objDict["__class__"], objDict["id"])
            try:
                self.__objects.pop(objDict)
            except:
                pass
