from math import ceil
from typing import Optional, List
from sqlalchemy.orm import Session
from app.blogs import models, schemas, utils


def _create(db: Session, instance):
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def get_category_query(db: Session, skip: int = 0, limit: int = 100):
    """get category list"""
    return db.query(models.Category).order_by(models.Category.id.desc()).offset(skip).limit(limit).all()


def get_category(db: Session, name: str):
    """get category by name"""
    return db.query(models.Category).filter(models.Category.name == name).first()


def create_category(db: Session, args: schemas.CreateCategory):
    """create category"""
    instance = models.Category(**args.dict())
    return _create(db, instance)


def get_series_query(db: Session, skip: int = 0, limit: int = 100):
    """get series list"""
    return db.query(models.Series).order_by(models.Series.id.desc()).offset(skip).limit(limit).all()


def get_series(db: Session, name: str):
    """get series by name"""
    return db.query(models.Series).filter(models.Series.name == name).first()


def create_series(db: Session, args: schemas.CreateSeries):
    """create series"""
    instance = models.Series(**args.dict())
    return _create(db, instance)


def get_tag_query(db: Session, skip: int = 0, limit: int = 100):
    """get tag list"""
    return db.query(models.Tag).order_by(models.Tag.id.desc()).offset(skip).limit(limit).all()


def get_tag(db: Session, name: str):
    """get tag by name"""
    return db.query(models.Tag).filter(models.Tag.name == name).first()


def get_tag_by_id(db: Session, _id: int):
    """get tag by id"""
    return db.query(models.Tag).filter(models.Tag.id == _id).first()


def create_tag(db: Session, args: schemas.CreateTag):
    """create tag"""
    instance = models.Tag(**args.dict())
    return _create(db, instance)


def get_post(db: Session, post_id: int):
    """get post by id"""
    return db.query(models.Post).filter(models.Post.id == post_id).first()


def filter_post_by_category(db: Session, category_id: int):
    """get post list by category"""
    return db.filter(models.Post.category_id == category_id)


def filter_post_by_series(db: Session, series_id: int):
    """get post list by series"""
    return db.filter(models.Post.series_id == series_id)


def filter_post_by_tag(db: Session, tag_id: int):
    """get post list by tag"""
    return db.filter(models.Post.tag.any(models.Tag.id == tag_id))


def filter_post_by_tags(db: Session, tag_ids: List[int]):
    """get post list by tag"""
    for tag_id in tag_ids:
        db = db.filter(models.Post.tag.any(models.Tag.id == tag_id))
    return db


def filter_post_by_is_public(db: Session):
    return db.filter(models.Post.is_public == True)


def get_post_query(
    db: Session,
    category_id: Optional[int] = None,
    series_id: Optional[int] = None,
    tag_ids: Optional[List[int]] = None,
    is_private: Optional[bool] = True,
    skip: int = 0,
    limit: int = 100,
):
    """get post list
    filter_by:
    - category id
    - series id
    - tag id
    - is_private
    """
    db = db.query(models.Post)
    db = filter_post_by_is_public(db) if not is_private else db
    db = filter_post_by_category(db, category_id) if category_id is not None else db
    db = filter_post_by_series(db, series_id) if series_id is not None else db
    db = filter_post_by_tags(db, tag_ids) if tag_ids is not None else db
    total = db.count()
    max_page = ceil(total / limit)
    query = db.order_by(models.Post.public_at.desc(), models.Post.id.desc()).offset(skip).limit(limit).all()
    return query, max_page, total


def create_post(db: Session, post: schemas.CreatePost):
    post_dict = post.dict()
    if post_dict.pop("tag_ids"):
        post_dict["tag"] = [get_tag_by_id(db, ids) for ids in post.tag_ids]

    instance = models.Post(**post_dict)
    instance = _create(db, instance)
    return instance


def get_tags(db: Session, tag_ids: List[int]) -> List[models.Tag]:
    tags = []
    for tag_id in tag_ids:
        tag = get_tag_by_id(db, tag_id)
        if tag:
            tags.append(tag)
        else:
            raise KeyError('some tag id is invalid')
    return tags


def update_post(db: Session, base_post: models.Post, post: utils.UpdateIDPost):
    base_post.update_dict(post.to_items())

    if post.tag_ids is not None:
        base_post.tag = get_tags(db, post.tag_ids)

    db.commit()
    db.refresh(base_post)
    return base_post


def delete_post(db: Session, post_id: int):
    post = db.query(models.Post).filter(models.Post.id == post_id)
    post.delete()
    db.commit()


def get_comment(db: Session, comment_id: int):
    """get comment by id"""
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()


def get_comment_query(
    db: Session, post_id: Optional[int] = None, skip: int = 0, limit: int = 100
):
    """get comments by post id"""
    db = db.query(models.Comment).filter(models.Comment.post_id == post_id)
    return db.offset(skip).limit(limit).all()


def create_comment(db: Session, comment: schemas.CreateComment, author_id: int):
    instance = models.Comment(**comment.dict(), author_id=author_id)
    instance = _create(db, instance)
    return instance


def delete_comment(db: Session, comment_id: int):
    comment = db.query(models.Comment).filter(models.Comment.id == comment_id)
    comment.delete()
    db.commit()
