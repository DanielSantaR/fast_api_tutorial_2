from pydantic import BaseModel, EmailStr
from typing import Optional


class OwnerBase(BaseModel):
    name: str
    surname: Optional[str]
    username: str
    email: EmailStr

    class Config:
        orm_mode = True


class OwnerOut(OwnerBase):
    id: int
    pass


class Owner(OwnerBase):
    password: str


class OwnerUpdate(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    username: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
