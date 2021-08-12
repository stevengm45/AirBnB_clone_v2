#!/usr/bin/python3
"""
   This is the Place class
"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from os import getenv as env


place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id', String(60),
                             ForeignKey('places.id')),
                      Column('amenity_id', String(60),
                             ForeignKey('amenities.id')))


class Place(BaseModel, Base):
    """
    Class Place that defines the place where the service is offer
    """
    __tablename__ = "places"

    if env("HBNB_TYPE_STORAGE") == "db":
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        kwargs = {"cascade": "all, delete-orphan", "backref": "place"}
        reviews = relationship("Review", **kwargs)
        # Dictinary for each relationship.
        kwargs = {"secondary": place_amenity,
                  "back_populates": "place_amenities",
                  "viewonly": False}
        amenities = relationship("Amenity", **kwargs)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """ Returns the list of City instances with state_id. """
            objDict = FileStorage.all()
            reviewList = []
            for key, obj in objDict:
                if obj.place_id == self.id:
                    reviewList.append(obj)
            return (reviewList)

        @property
        def amenities(self):
            """ Returns the list of Amenity instances related with place. """
            objDict = FileStorage.all()
            amenityList = []
            for key, obj in objDict:
                if obj.place_id == self.id:
                    amenityList.append(obj)
            return (amenityList)

        @amenities.setter
        def amenities(self, cls):
            """ Sets the value of amenity_ids attribute. """
            if cls.__class__.__name__ == "Amenity":
                self.amenity_ids.append(cls.id)
