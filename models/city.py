#!/user/bin/python3
"""
   This is the City class
"""
from models.base_model import BaseModel


class City(BaseModel):
    """
    Class City that defines the city where the service is offer
    """
    state_id = ""
    name = ""
