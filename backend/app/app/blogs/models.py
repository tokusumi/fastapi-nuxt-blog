from sqlalchemy import (
    Boolean,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
    text,
    Text,
    Table,
)
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import relationship
from app.db.base import Base


class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())

    def __repr__(self):
        return self.name


class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    post = relationship("Post", secondary=lambda: post__tag, backref="tags")

    def __repr__(self):
        return self.name


post__tag = Table(
    "post__tag",
    Base.metadata,
    Column("tag_id", Integer, ForeignKey("tag.id")),
    Column("post_id", Integer, ForeignKey("post.id")),
)


class Series(Base):
    __tablename__ = "series"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())

    def __repr__(self):
        return self.name


class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(Text)
    image = Column(String, default="")
    author_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    author = relationship("User", backref="posts")
    series_id = Column(Integer, ForeignKey("series.id"), nullable=True)
    series = relationship("Series", backref="posts")
    category_id = Column(Integer, ForeignKey("category.id"), nullable=True)
    category = relationship("Category", backref="posts")
    tag = relationship("Tag", secondary=lambda: post__tag, backref="posts")
    public_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    # updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    is_public = Column(Boolean, default=False)
    notification = Column(Boolean, default=False)

    def __repr__(self):
        return self.title

    def update_dict(self, dict):
        for name, value in dict.items():
            if name in self.__dict__:
                setattr(self, name, value)


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    author = relationship("User", backref="comments")
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    body = Column(String)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
