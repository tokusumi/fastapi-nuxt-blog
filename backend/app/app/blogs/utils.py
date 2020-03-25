from sqlalchemy.orm import Session
from app.blogs import schemas, crud


class BaseNameToId:
    def __init__(self, db: Session, data: schemas.BaseModel):
        self.db = db
        self.data = data

    def to_items(self):
        raise NotImplementedError

    @property
    def category_id(self):
        q = crud.get_category(self.db, self.data.category)
        return q.id if q is not None else None

    @property
    def series_id(self):
        q = crud.get_series(self.db, self.data.series)
        return q.id if q is not None else None

    @property
    def tag_id(self):
        q = crud.get_tag(self.db, self.data.tag)
        return q.id if q is not None else None

    @property
    def tag_ids(self):
        if isinstance(self.data.tags, list):
            qs = [crud.get_tag(self.db, tag) for tag in self.data.tags]
            return [q.id for q in qs if q]
        return None


class FilterIDPost(BaseNameToId):
    def __init__(self, db: Session, data: schemas.FilterPost):
        self.db = db
        self.data = data

    def to_items(self):
        return {
            "category_id": self.category_id,
            "series_id": self.series_id,
            "tag_ids": self.tag_ids,
        }


class CreateIDPost(BaseNameToId):
    def __init__(self, db: Session, CreatePostReq: schemas.CreatePostReq):
        self.db = db
        self.data = CreatePostReq

    def to_items(self):
        ids = {
            "category_id": self.category_id,
            "series_id": self.series_id,
            "tag_ids": self.tag_ids,
        }
        return dict(
            **ids,
            **{
                f: g
                for f, g in self.data.dict().items()
                if f not in ["category", "series", "tags"]
            }
        )


class UpdateIDPost(BaseNameToId):
    def __init__(self, db: Session, UpdatePost: schemas.UpdatePost):
        self.db = db
        self.data = UpdatePost

    def to_items(self):
        ids = {
            "category_id": self.category_id,
            "series_id": self.series_id,
            "tag_ids": self.tag_ids,
        }
        _dict = dict(
            **ids,
            **{
                f: g
                for f, g in self.data.dict().items()
                if f not in ["category", "series", "tags"]
            }
        )
        return {f: g for f, g in _dict.items() if g is not None}
