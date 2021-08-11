#!/usr/bin/python3
"""
    This is the base class of all models
"""
import models
from sqlalchemy import Column, String, Integer, MetaData, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from os import getenv as env
import uuid

Base = declarative_base()


time = "%Y-%m-%dT%H:%M:%S.%f"

class BaseModel:
    """
    Class BaseModel that defines all common attributes
    and methods for other classes
    """
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow())
    updated_at = Column(DateTime, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            from models import storage
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            if env("HBNB_TYPE_STORAGE") != "db":
                storage.new(self)
        else:
            # Add the "id" attribute if not in kwargs.
            if "id" not in kwargs:
                kwargs["id"] = self.id = str(uuid.uuid4())

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
        """
            Method that update the public instance attribute with the
            current datetime
        """
        self.updated_at = datetime.utcnow()
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
        """delete the current instance from the storage"""
        models.storage.delete(self)
