from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils import EmailType
from db.database import Base
import datetime


class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(EmailType, unique=True)

    #pet_id = Column(Integer, ForeignKey("pets.id"))

    #pets = relationship("Pet", back_populates="owner")


class Pet(Base):
    __tablename__ = "pets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    pet_type = Column(String)
    breed = Column(String)
    picture = Column(String)
    create_date = Column(DateTime)
    update_date = Column(DateTime)
    is_adopted = Column(Boolean)
    age = Column(Integer)
    weight = Column(Integer)

    #owner_id = Column(Integer, ForeignKey("owners.id"))

    #owner = relationship("Owner", back_populates="pets")
