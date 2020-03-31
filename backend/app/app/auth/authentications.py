from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from jwt import PyJWTError
from app.users.crud import get_user_by_email_query
from app.settings import configs as conf
from app.db.session import get_db
from app.auth import schemas, token


async def get_token_data(access_token: str = Depends(conf.OAUTH2_SCHEME)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = token.validate_access_token(access_token)
        if payload is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = schemas.TokenData(**payload)
    except PyJWTError:
        raise credentials_exception
    return token_data


async def get_current_user(
    db: Session = Depends(get_db),
    token_data: schemas.TokenData = Depends(get_token_data),
):
    user = get_user_by_email_query(db, email=token_data.username)
    if user is None:
        raise HTTPException(
            status_code=400,
            detail="does not exist",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: schemas.User = Depends(get_current_user),
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
