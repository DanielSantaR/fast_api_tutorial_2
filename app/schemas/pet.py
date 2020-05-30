from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class BasePet(BaseModel):
    pet_type: str
    breed: Optional[str]
    is_adopted: Optional[bool]
    age: Optional[int]
    weight: Optional[float]
    owner_id: int

    class Config:
        orm_mode = True


class Pet(BasePet):
    id: int
    name: str
    picture: Optional[str]
    create_date: datetime
    update_date: datetime


class UpdatePet(BaseModel):
    name: Optional[str]
    picture: Optional[bool]
    breed: Optional[str]
    is_adopted: Optional[bool]
    age: Optional[int]
    weight: Optional[float]

