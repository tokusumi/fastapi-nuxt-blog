from typing import Optional, List
from pydantic import BaseModel


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


class Friend(UserBase):
    id: int
    is_active: bool
    icon: str

    class Config:
        orm_mode = True


class User(UserBase):
    id: int
    username: str
    is_active: bool
    icon: str
    invite_code: Optional[str] = None
    friends: Optional[List[Friend]] = None

    class Config:
        orm_mode = True


class Author(UserBase):
    id: int
    username: str
    is_active: bool
    icon: str

    class Config:
        orm_mode = True


class SuccessSchema(BaseModel):
    result: bool = True
