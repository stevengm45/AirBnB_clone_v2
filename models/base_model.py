#!/usr/bin/python3
"""
    This is the base class of all models
"""
import models
from datetime import datetime
import sqlalchemy
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

if models.storage_t == "db":
    Base = declarative_base()
else:
    Base = object

time = "%Y-%m-%dT%H:%M:%S.%f"

class BaseModel:
    """
    Class BaseModel that defines all common attributes
    and methods for other classes
    """
    if models.storage_t == "db":
        id = Column(String(60), primary_key=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """
            __init__ method to initialize the BaseModel
            isinstance
        """
        
        """Initialization of the base model"""
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
                self.id = str(uuid.uuid4())
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

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
        
    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
