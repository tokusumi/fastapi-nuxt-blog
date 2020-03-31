from starlette.testclient import TestClient
from app.main import app
from app.db.session import get_db
from app.auth import schemas as auth_schemas
from app.users.crud import create_user_query
from app.users.schemas import UserCreate
from app.auth.main import (
    get_authenticated_user,
    get_token_data,
    login_for_access_token
)

client = TestClient(app)


def pytest_db(f):
    """decorator to use temporary database
    if this decorates testing function,
    testing api connects temporary database,
    which is isolated all others testing and existing database.
    NOTE: must define SessionLocal fixture in conftest.py
    """

    def func(SessionLocal, *args, **kwargs):
        def override_get_db():
            try:
                db = SessionLocal()
                yield db
            finally:
                db.close()

        app.dependency_overrides[get_db] = override_get_db
        f(SessionLocal, *args, **kwargs)

        app.dependency_overrides[get_db] = get_db

    return func


def test_get_authenticated_user(SessionLocal):
    db = SessionLocal()
    user_data = {'username': 'test user',
                 'email': 'test@example.com',
                 'password': 'test1234'}

    user_scheme = UserCreate(**user_data)
    create_user_query(db, user_scheme)

    # success
    user = get_authenticated_user(db, user_data['email'], user_data['password'])
    assert user.username == user_data['username']

    # user does not exist
    user = get_authenticated_user(db, 'no', user_data['password'])
    assert user is None

    # invalid password
    user = get_authenticated_user(db, user_data['email'], 'no')
    assert user is None


@pytest_db
def test_token_auth(SessionLocal):
    db = SessionLocal()
    user_data = {'username': 'test user',
                 'email': 'test@example.com',
                 'password': 'test1234'}

    user_scheme = UserCreate(**user_data)
    create_user_query(db, user_scheme)

    res = client.post(
        '/auth/token',
        data=(
            # data
            b"--a7f7ac8d4e2e437c877bb7b8d7cc549c\r\n"
            b'Content-Disposition: form-data; name="username"\r\n\r\n'
            b"test@example.com\r\n"
            # data
            b"--a7f7ac8d4e2e437c877bb7b8d7cc549c\r\n"
            b'Content-Disposition: form-data; name="password"\r\n\r\n'
            b"test1234\r\n"
            b"--a7f7ac8d4e2e437c877bb7b8d7cc549c--\r\n"
        ),
        headers={
            "Content-Type": "multipart/form-data; boundary=a7f7ac8d4e2e437c877bb7b8d7cc549c"
        },
    )
    assert res.status_code == 200

    res = client.post(
        '/auth/token',
        data=(
            # data
            b"--a7f7ac8d4e2e437c877bb7b8d7cc549c\r\n"
            b'Content-Disposition: form-data; name="username"\r\n\r\n'
            b"test@example.com\r\n"
            # data
            b"--a7f7ac8d4e2e437c877bb7b8d7cc549c\r\n"
            b'Content-Disposition: form-data; name="password"\r\n\r\n'
            b"incorrect\r\n"
            b"--a7f7ac8d4e2e437c877bb7b8d7cc549c--\r\n"
        ),
        headers={
            "Content-Type": "multipart/form-data; boundary=a7f7ac8d4e2e437c877bb7b8d7cc549c"
        },
    )
    assert res.status_code == 401
