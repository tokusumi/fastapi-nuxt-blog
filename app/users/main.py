from typing import List

from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session

from . import models, schemas
from .crud import (
    get_user_by_email_query,
    get_user_by_password_query,
    get_users_query,
    create_user_query,
    delete_user_query
)
from settings.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = APIRouter()


# Dependency
def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/users/", response_model=List[schemas.User], tags=['user'])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_user = get_users_query(db, skip=skip, limit=limit)
    if len(db_user) == 0:
        raise HTTPException(status_code=400, detail="User does not exist")
    return db_user


@app.post("/users/", response_model=schemas.User, tags=['user'])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email_query(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user_query(db=db, user=user)


@app.delete("/users/", response_model=schemas.User, tags=['user'])
def delete_user(user: schemas.UserDelete, db: Session = Depends(get_db)):
    db_user = get_user_by_password_query(db, email=user.email, password=user.password)
    if not db_user:
        raise HTTPException(status_code=400, detail="Does not exist")
    delete_user_query(db, db_user)
    return db_user
