#!/user/bin/python3
"""
   This is the City class
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv as env


class City(BaseModel, Base):
    """ The city class, contains state ID and name """
    __tablename__ = "cities"
    if env("HBNB_TYPE_STORAGE") == "db":
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
        kwargs = {"cascade": "all, delete-orphan", "backref": "cities"}
        places = relationship("Place", **kwargs)
    else:
        place_id = ""
        user_id = ""
        text = ""
