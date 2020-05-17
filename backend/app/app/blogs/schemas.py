from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime
from app.users.schemas import Author


class Success(BaseModel):
    success: bool = True


class Image(BaseModel):
    image: str


class CreateCategory(BaseModel):
    name: str


class Category(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class CreateSeries(BaseModel):
    name: str


class Series(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class CreateTag(BaseModel):
    name: str


class Tag(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class BasePost(BaseModel):
    title: str = ""
    image: str = ""
    body: Optional[str] = None
    is_public: bool = False
    notification: bool = False
    public_at: datetime


class CreatePost(BasePost):
    author_id: int
    category_id: Optional[int] = None
    series_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None


class CreatePostReq(BasePost):
    category: Optional[str] = None
    series: Optional[str] = None
    tags: Optional[List[str]] = None


class BaseUpdatePost(BaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    body: Optional[str] = None
    is_public: Optional[bool] = None
    notification: Optional[bool] = None
    public_at: Optional[datetime] = None


class UpdatePostReq(BaseUpdatePost):
    category: Optional[str] = None
    series: Optional[str] = None
    tags: Optional[List[str]] = None


class UpdatePost(BaseUpdatePost):
    category_id: Optional[int] = None
    series_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None


class FilterPost(BaseModel):
    author: Optional[str] = None
    category: Optional[str] = None
    series: Optional[str] = None
    tags: Optional[List[str]] = None
    is_private: Optional[bool] = True
    public_at: Optional[datetime] = None


class Post(BasePost):
    id: int
    author: Author
    category: Category = None
    series: Series = None
    tags: List[Tag] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class Posts(BaseModel):
    data: List[Post]
    max_page: int
    total: int


class BaseComment(BaseModel):
    pass


class CreateComment(BaseModel):
    post_id: int
    body: str


class Comment(BaseComment):
    id: int
    post_id: int
    author: Author
    body: str
    created_at: datetime

    class Config:
        orm_mode = True
