from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime


class Success(BaseModel):
    success: bool = True


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
    title: str
    body: str
    is_public: bool = False
    notification: bool = False


class CreatePost(BasePost):
    author_id: int
    category_id: Optional[int] = None
    series_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None


class CreatePostReq(BasePost):
    category: Optional[str] = None
    series: Optional[str] = None
    tags: Optional[List[str]] = None


class FilterPost(BaseModel):
    author: Optional[str] = None
    category: Optional[str] = None
    series: Optional[str] = None
    tags: Optional[List[str]] = None


class Post(BasePost):
    id: int
    author: str
    category: Optional[str] = None
    series: Optional[str] = None
    tags: Optional[List[str]] = None

    class Config:
        orm_mode = True

    def author(self):
        return self.author.name

    def category(self):
        return self.category.name

    def series(self):
        return self.series.name

    def tags(self):
        return [tag.name for tag in self.tags]


class BaseComment(BaseModel):
    pass


class CreateComment(BaseModel):
    post_id: int
    body: str


class Comment(BaseComment):
    id: int
    post_id: int
    author: str
    body: str
    created_at: datetime

    class Config:
        orm_mode = True

    def author(self):
        return self.author.name
