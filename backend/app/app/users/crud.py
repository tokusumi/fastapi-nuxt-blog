from datetime import datetime
from sqlalchemy.orm import Session
from app.auth.token import verify_password, get_password_hash
from app.users import models, schemas
from app.images.process import hash_string


def get_user_by_id_query(db: Session, user_id: int):
    """get user by user id"""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email_query(db: Session, email: str):
    """get user by email"""
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_password_query(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def get_users_query(db: Session, skip: int = 0, limit: int = 100):
    """get user list"""
    return db.query(models.User).order_by(models.User.id.desc()).offset(skip).limit(limit).all()


def create_user_query(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email, username=user.username, hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, base_user: models.User, user: schemas.UserUpdate):
    is_update = base_user.update_dict({key: val for key, val in user.dict().items() if val is not None})
    if is_update:
        db.commit()
        db.refresh(base_user)
    return base_user, is_update


def delete_user_query(db: Session, user: Session.query):
    db.delete(user)
    db.commit()


def get_invitee(db: Session, invite_code: str):
    """TODO:"""
    return db.query(models.User).filter(models.User.invite_code == invite_code).first()


def append_friend(db: Session, user: models.User, friend: models.User):
    is_updated = user.befriend(friend)
    if is_updated:
        db.commit()
        db.refresh(user)
    return user, is_updated


def recreate_and_update_invite_code(db: Session, user: models.User):
    now = datetime.now().strftime("%T%Y%m%d%s")
    invite_code = hash_string(user.email + now)
    user.invite_code = invite_code
    db.commit()
    db.refresh(user)
    return user
