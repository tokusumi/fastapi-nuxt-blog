import pytest
from fastapi import HTTPException
from app.auth.token import add_access_token
from app.auth import schemas
from app.auth.authentications import (
    get_token_data,
    get_current_user,
    get_current_active_user
)
from app.users.crud import create_user_query
from app.users.schemas import UserCreate


@pytest.mark.asyncio
async def test_get_token_data():
    data = {'username': 'test user'}

    token_data = schemas.TokenData(**data)
    jwt = add_access_token(token_data)

    token_data = await get_token_data(access_token=jwt)
    token_data = token_data.dict()
    assert all([token_data[key] == data[key] for key in data])


@pytest.mark.asyncio
async def test_get_expired_token_data_error():
    data = {'username': 'test user'}

    token_data = schemas.TokenData(**data)
    jwt = add_access_token(token_data, expire_min=0)

    try:
        exception = False
        token_data = await get_token_data(access_token=jwt)
    except HTTPException:
        exception = True
    assert exception, 'Must raise with expiration'


@pytest.mark.asyncio
async def test_get_invalid_token_data_error():
    jwt = 'invalid token'

    try:
        exception = False
        await get_token_data(access_token=jwt)
    except HTTPException:
        exception = True
    assert exception, 'Must raise with invalid credentials'


@pytest.mark.asyncio
async def test_get_current_user(SessionLocal):
    user_data = {'username': 'test user', 'email': 'test@example.com', 'password': 'test1234'}
    db = SessionLocal()

    user_scheme = UserCreate(**user_data)
    created_user_res = create_user_query(db, user_scheme)
    assert created_user_res

    token_data = schemas.TokenData(username=user_data['email'])
    current_user = await get_current_user(db=db, token_data=token_data)
    assert current_user.email == user_data['email']


@pytest.mark.asyncio
async def test_not_exist_get_current_user(SessionLocal):
    db = SessionLocal()
    user_data = {'username': 'anonymouse user', 'email': 'anno@example.com', 'password': 'anonymous'}

    token_data = schemas.TokenData(**user_data)
    try:
        exception = False
        await get_current_user(db=db, token_data=token_data)
    except HTTPException:
        exception = True
    assert exception, 'Must raise for token data does not exist'


@pytest.mark.asyncio
async def test_get_current_active_user():
    user_data = {'id': 1, 'username': 'test user',
                 'email': 'test@example.com', 'password': 'test1234', 'is_active': True}
    user = schemas.User(**user_data)

    active_user = await get_current_active_user(user)
    assert active_user is user


@pytest.mark.asyncio
async def test_get_current_inactive_user():
    user_data = {'id': 1, 'username': 'test user', 'email': 'test@example.com',
                 'password': 'test1234', 'is_active': False}
    user = schemas.User(**user_data)

    try:
        exception = False
        await get_current_active_user(user)
    except HTTPException:
        exception = True
    assert exception, 'Must active user is returned'
