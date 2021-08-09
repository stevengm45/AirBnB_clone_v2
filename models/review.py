#!/usr/bin/python3
"""
    This is the Review class
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """
    Class Review that defines the reviews the offer service
    """
    place_id = ""
    user_id = ""
    text = ""
