from sqlalchemy.orm import Session
from . import models, schemas


def _create(db: Session, instance):
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


def get_category_query(db: Session, skip: int = 0, limit: int = 100):
    """get category list"""
    return db.query(models.Category).offset(skip).limit(limit).all()


def get_category(db: Session, name: str):
    """get category by name"""
    return db.query(models.Category).filter(models.Category.name == name).first()


def create_category(db: Session, args: schemas.CreateCategory):
    """create category"""
    instance = models.Category(**args.dict())
    return _create(db, instance)


def get_series_query(db: Session, skip: int = 0, limit: int = 100):
    """get series list"""
    return db.query(models.Series).offset(skip).limit(limit).all()


def get_series(db: Session, name: str):
    """get series by name"""
    return db.query(models.Series).filter(models.Series.name == name).first()


def create_series(db: Session, args: schemas.CreateSeries):
    """create series"""
    instance = models.Series(**args.dict())
    return _create(db, instance)


def get_tag_query(db: Session, skip: int = 0, limit: int = 100):
    """get tag list"""
    return db.query(models.Tag).offset(skip).limit(limit).all()


def get_tag(db: Session, name: str):
    """get tag by name"""
    return db.query(models.Tag).filter(models.Tag.name == name).first()


def create_tag(db: Session, args: schemas.CreateTag):
    """create tag"""
    instance = models.Tag(**args.dict())
    return _create(db, instance)
