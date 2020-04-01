from typing import List

from fastapi import Depends, APIRouter, HTTPException, UploadFile, File
from sqlalchemy.orm import Session

from app.users import models, schemas
from app.users.crud import (
    get_user_by_id_query,
    get_user_by_email_query,
    get_user_by_password_query,
    get_users_query,
    create_user_query,
    update_user,
    delete_user_query,
    get_invitee,
    append_friend,
    recreate_and_update_invite_code
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
def create_user(
    user: schemas.UserCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    db_user = get_user_by_email_query(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user_query(db=db, user=user)


@app.put("/users/", response_model=schemas.User, tags=["user"])
def update_users(
    user: schemas.UserUpdate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    current_user = get_user_by_id_query(db, current_user.id)
    new_user, is_update = update_user(db, current_user, user)
    if not is_update:
        raise HTTPException(status_code=400, detail="only same value")
    return new_user


@app.delete("/users/", response_model=schemas.User, tags=["user"])
def delete_user(
    user: schemas.UserDelete,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    db_user = get_user_by_password_query(db, email=user.email, password=user.password)

    if not db_user:
        raise HTTPException(status_code=400, detail="Does not exist")
    delete_user_query(db, db_user)
    return db_user


@app.get("/users/me/", response_model=schemas.User, tags=['user'])
async def read_users_me(current_user: schemas.User = Depends(get_current_active_user)):
    return current_user


@app.post("/users/image/", response_model=schemas.User, tags=['user'])
async def add_icon(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    new_user = await process_image.save_and_add_icon(file, current_user.id, db)
    return new_user


@app.get("/users/friend/reflesh/invite_code/", response_model=schemas.User, tags=['user'])
async def reflesh_invite_code(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    current_user = get_user_by_id_query(db, current_user.id)
    return recreate_and_update_invite_code(db, current_user)


@app.get("/users/friend/{invite_code}/", response_model=schemas.User, tags=['user'])
async def add_friend(
    invite_code: str,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(get_current_active_user),
):
    invitee = get_invitee(db, invite_code)
    user, is_updated = append_friend(db, current_user, invitee)
    if not is_updated:
        raise HTTPException(status_code=400, detail="Already being friend")
    return user
