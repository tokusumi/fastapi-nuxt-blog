from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str


class TokenData(BaseModel):
    username: str


class TokenFullData(TokenData):
    exp: datetime


class User(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    is_active: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


class FormData(BaseModel):
    username: str
    password: str
