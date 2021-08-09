#!/usr/bin/python3
"""
This is class User
"""
from models.base_model import BaseModel


class User(BaseModel):
    """class User display the information of user"""
    email = ""
    password = ""
    first_name = ""
    last_name = ""
