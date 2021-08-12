#!/usr/bin/python3
"""
    This is the base class of all models
"""
import models
from datetime import datetime
from sqlalchemy import Column, String, Integer, MetaData, DateTime
from sqlalchemy.ext.declarative import declarative_base

from uuid import uuid4

time = "%Y-%m-%dT%H:%M:%S.%f"
Base = declarative_base()

class BaseModel:
    """
    Class BaseModel that defines all common attributes
    and methods for other classes
    """
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
            __init__ method to initialize the BaseModel
            isinstance
        """
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get("created_at", None) and type(self.created_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("updated_at", None) and type(self.updated_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = str(uuid4())
        else:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at
        """
        if not kwargs:
            from models import storage
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            if env("HBNB_TYPE_STORAGE") != "db":
                storage.new(self)
        else:
            # Add the "id" attribute if not in kwargs.
            if "id" not in kwargs:
                kwargs["id"] = self.id = str(uuid4())

            # Add the "updated at" attribute if not in kwargs.
            if "updated_at" not in kwargs:
                kwargs["updated_at"] = datetime.now().isoformat()
            kwargs['updated_at'] = datetime.strptime(kwargs['updated_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            # Add the "created at" attribute if not in kwargs.
            if "created_at" not in kwargs:
                kwargs["created_at"] = datetime.now().isoformat()
            kwargs['created_at'] = datetime.strptime(kwargs['created_at'],
                                                     '%Y-%m-%dT%H:%M:%S.%f')
            if '__class__' in kwargs:
                del kwargs['__class__']
            self.__dict__.update(kwargs)

    def __str__(self):
        """
            Method that return the string representation of current object
        """
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        dictionary.pop("_sa_instance_state", None)
        return dictionary

    def delete(self):
        """Delete the current instance from the storage"""
        models.storage.delete()
