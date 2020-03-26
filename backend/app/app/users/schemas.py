from typing import Optional

from pydantic import BaseModel
from fastapi import UploadFile


class UserBase(BaseModel):
    email: str
    username: str = ""


class UserCreate(UserBase):
    password: str


class UserDelete(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    icon: Optional[str] = None


class User(UserBase):
    id: int
    username: str
    is_active: bool
    icon: str

    class Config:
        orm_mode = True


class SuccessSchema(BaseModel):
    result: bool = True
