from typing import Optional
from datetime import datetime, timedelta
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jwt import PyJWTError
from app.settings import configs as conf
from app.db.session import get_db
from app.auth import schemas, token


app = APIRouter()


def get_authenticated_user(db: Session, email: str, password: str):
    """validate password and return user
    require: columns in conf.USER_MODEL
    - email
    - hashed_password
    """
    user = db.query(conf.USER_MODEL).filter(conf.USER_MODEL.email == email).first()
    if not user:
        return None
    if token.verify_password(password, user.hashed_password):
        return user


def get_token_data(user, token_schema):
    data = {"username": user.email}
    return token_schema(**data)


@app.post("/auth/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    # form_data: schemas.FormData,
    db: Session = Depends(get_db),
):
    user = get_authenticated_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token_data = get_token_data(user, schemas.TokenData)
    access_token = token.add_access_token(token_data=token_data)
    return {"access_token": access_token}
