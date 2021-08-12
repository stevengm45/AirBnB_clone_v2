
#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models.engine.file_storage import FileStorage
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, backref
from os import getenv as env


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    if env("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        kwargs = {"cascade": "all, delete-orphan", "backref": "state"}
        cities = relationship("City", **kwargs)
    else:
        name = ""

        @property
        def cities(self):
            """returns the list of City instances with state_id"""
            objDict = FileStorage().all()
            citiesList = []
            for key, value in objDict.items():
                try:
                    if value.state_id == self.id:
                        citiesList.append(value)
                except:
                    pass
            return (citiesList)