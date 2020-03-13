from sqlalchemy.orm import Session
from hashlib import md5 as hash_func
from . import models, schemas


def get_user_by_id_query(db: Session, user_id: int):
    """get user by user id"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email_query(db: Session, email: str):
    """get user by email"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_password_query(db: Session, email: str, password: str):
    hashed_password = hash_func(password.encode()).hexdigest()
    return db.query(models.User).filter(models.User.email == email, models.User.hashed_password == hashed_password).first()


def get_users_query(db: Session, skip: int = 0, limit: int = 100):
    """get user list"""
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user_query(db: Session, user: schemas.UserCreate):
    hashed_password = hash_func(user.password.encode()).hexdigest()
    db_user = models.User(email=user.email, name=user.name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user_query(db: Session, user: Session.query):
    db.delete(user)
    db.commit()
