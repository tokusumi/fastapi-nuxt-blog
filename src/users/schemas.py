from typing import Optional

from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str = ""


class UserCreate(UserBase):
    password: str


class UserDelete(UserBase):
    password: str


class UserUpdate(UserBase):
    hased_password: Optional[str] = None
    is_active: Optional[bool] = None


class User(UserBase):
    id: int
    username: str
    is_active: bool

    class Config:
        orm_mode = True
