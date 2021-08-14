#!/usr/bin/python3
"""
    This is the base class of all models
"""
import models
from datetime import datetime
from uuid import uuid4


class BaseModel:
    """
    Class BaseModel that defines all common attributes
    and methods for other classes
    """
    def __init__(self, *args, **kwargs):
        """
            __init__ method to initialize the BaseModel
            isinstance
        """
        if kwargs:
            for key, value in kwargs.items():
                if key == '__class__':
                    pass

                elif key == "created_at" or key == "updated_at":
                    new_date = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                    setattr(self, key, new_date)

                else:
                    setattr(self, key, value)

        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            models.storage.new(self)

    def __str__(self):
        """
            Method that return the string representation of current object
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """
            Method that update the public instance attribute with the
            current datetime
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
            Method that return a dictionary with keys/values of __dict__
            of the instance and class name
        """
        dictionary = dict(self.__dict__)
        dictionary['__class__'] = str(type(self).__name__)
        dictionary['created_at'] = getattr(self, "created_at").isoformat()
        dictionary['updated_at'] = getattr(self, "updated_at").isoformat()
        return dictionary
