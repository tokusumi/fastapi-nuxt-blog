from pydantic import BaseModel


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
