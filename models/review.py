#!/usr/bin/python3
"""
    This is the Review class
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from os import getenv as env


class Review(BaseModel, Base):
    """
    Class Review that defines the reviews the offer service
    """
    __tablename__ = "reviews"
    place_id = ""
    user_id = ""
    text = ""
    if env("HBNB_TYPE_STORAGE") == "db":
        place_id = Column(String(60), ForeignKey("places.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        text = Column(String(1024), nullable=False)
