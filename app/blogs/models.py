from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, text, Text, Table
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.orm import relationship
from settings.database import Base


class Category(Base):
    __tablename__ = 'category'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())


class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    post = relationship("Post", secondary=lambda: post__tag, backref="tags")


post__tag = Table(
    'post__tag', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tag.id')),
    Column('post_id', Integer, ForeignKey('post.id'))
)


class Series(Base):
    __tablename__ = 'series'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())


class Post(Base):
    __tablename__ = 'post'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    body = Column(Text)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    series_id = Column(Integer, ForeignKey('series.id'), nullable=True)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=True)
    tag = relationship("Tag", secondary=lambda: post__tag, backref="posts")
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    # updated_at = Column(DateTime, nullable=False, server_default=text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    is_public = Column(Boolean, default=False)
    notification = Column(Boolean, default=False)


class Comment(Base):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True, index=True)
    author_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    created_at = Column(DateTime, nullable=False, server_default=current_timestamp())
    body = Column(Text(100))
    post_id = Column(Integer, ForeignKey('post.id'), nullable=False)
