from typing import List

from fastapi import Depends, APIRouter, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.users import models, schemas
from app.users.crud import (
    get_user_by_email_query,
    get_user_by_password_query,
    get_users_query,
    create_user_query,
    delete_user_query,
)
from app.db.session import get_db
from app.auth.authentications import get_current_active_user
from app.users import process_image


app = APIRouter()


@app.get("/users/", response_model=List[schemas.User], tags=["user"])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    db_user = get_users_query(db, skip=skip, limit=limit)
    if len(db_user) == 0:
        raise HTTPException(status_code=400, detail="User does not exist")
    return db_user


@app.post("/users/", response_model=schemas.User, tags=["user"])
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email_query(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user_query(db=db, user=user)


@app.delete("/users/", response_model=schemas.User, tags=["user"])
def delete_user(
    user: schemas.UserDelete,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    db_user = get_user_by_password_query(db, email=user.email, password=user.password)
    users = db.query(models.User).all()
    for user in users:
        print(user.email, user.hashed_password)

    if not db_user:
        raise HTTPException(status_code=400, detail="Does not exist")
    delete_user_query(db, db_user)
    return db_user


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


@app.post("/users/image/", response_model=schemas.SuccessSchema)
async def add_icon(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    await process_image.save_and_add_icon(file, current_user.id, db)

    return {"result": True}
