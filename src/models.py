from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional

db = SQLAlchemy()

"""
-------------------USER Table--------------------------------------------
"""
class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    fav: Mapped[List["FavoritePeople"]] = relationship(back_populates="userfav")
    favPlanet: Mapped[List["FavoritePlanet"]] = relationship(back_populates="userfav")
    
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "favorites Characters": [favorite.serialize() for favorite in self.fav],
            "favorites Planets": [favorite.serialize() for favorite in self.favPlanet]
            # do not serialize the password, it's a security breach
        }

"""
----------------------People Table-------------------------
"""
class People(db.Model):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=True)
    gender: Mapped[str] = mapped_column(String(120), nullable=True)
    age: Mapped[int] = mapped_column(Integer, nullable=True)

    
    favpeople: Mapped[List["FavoritePeople"]] = relationship()

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender
        self.age = age
        

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "age": self.age
        }

"""
-------------------------Planet Table----------------
"""
class Planet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=True)
    population: Mapped[int] = mapped_column(Integer, nullable=True)
    gravity: Mapped[int] = mapped_column(Integer, nullable=True)

  
    favplanet: Mapped[List["FavoritePlanet"]] = relationship()



    def __init__(self, name, population, gravity):
        self.name = name
        self.population = population
        self.gravity = gravity

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
            "gravity": self.gravity
        }

"""
----------------Favorites Table --------
"""
class FavoritePeople(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    userfav: Mapped["User"] = relationship(back_populates="fav")



    people_id:Mapped[Optional["People"]] = mapped_column(ForeignKey("people.id"), nullable=True)
    favpeople: Mapped[Optional["People"]] = relationship()

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "people_id": self.people_id,
        }

class FavoritePlanet(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    userfav: Mapped["User"] = relationship(back_populates="favPlanet")




    planet_id: Mapped[Optional["Planet"]] = mapped_column(ForeignKey("planet.id"), nullable=True)
    favplanet: Mapped[Optional["Planet"]] = relationship()

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id
        }