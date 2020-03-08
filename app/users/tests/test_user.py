from starlette.testclient import TestClient
from main import app
from users.main import get_db

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
        f(*args, **kwargs)

        app.dependency_overrides[get_db] = get_db
    return func


@pytest_db
def test_create_user():
    """
    create user
    """
    response = client.post(
        "/users/", json={"email": "foo1", "name": "fooo1", "password": "fo1"}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "email": "foo1",
        "name": "fooo1",
        "is_active": True,
    }


@pytest_db
def test_get_user():
    """
    create user
    """
    response = client.post(
        "/users/", json={"email": "foo1", "name": "fooo1", "password": "fo1"}
    )
    assert response.status_code == 200
    response = client.post(
        "/users/", json={"email": "foo2", "name": "fooo2", "password": "fo2"}
    )
    assert response.status_code == 200
    response = client.post(
        "/users/", json={"email": "foo3", "name": "fooo3", "password": "fo3"}
    )
    assert response.status_code == 200
    """
    get all users
    """
    # default
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 3

    # check skip
    response = client.get("/users/?skip=1")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["email"] == "foo2"

    # check limit
    response = client.get("/users/?limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["email"] == "foo1"


@pytest_db
def test_delete_user():
    """
    delete user
    """
    response = client.post(
        "/users/", json={"email": "foo1", "name": "fooo1", "password": "fo1"}
    )
    assert response.status_code == 200
    response = client.post(
        "/users/", json={"email": "foo2", "name": "fooo2", "password": "fo2"}
    )
    response = client.delete("/users/", json={"email": "foo1", "password": "fo1"})
    assert response.status_code == 200
    response = client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0] == {
        "id": 2,
        "email": "foo2",
        "name": "fooo2",
        "is_active": True,
    }
