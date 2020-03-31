from starlette.testclient import TestClient
from app.main import app
from app.blogs import crud, schemas
from app.db.session import get_db
from app.auth.authentications import get_current_active_user
from app.auth import schemas as auth_schemas

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

        def override_user():
            return auth_schemas.User(
                id="1", username="foo11", email="foo1", password="fo1", is_active=True
            )

        app.dependency_overrides[get_db] = override_get_db
        app.dependency_overrides[get_current_active_user] = override_user
        f(*args, **kwargs)

        app.dependency_overrides[get_db] = get_db

    return func


@pytest_db
def test_create_category():
    """
    create category
    """
    response = client.post("/category/", json={"name": "cat1"})
    assert response.status_code == 200


@pytest_db
def test_get_category():
    """
    create category
    """
    response = client.post("/category/", json={"name": "cat1"})
    assert response.status_code == 200
    response = client.post("/category/", json={"name": "cat2"})
    assert response.status_code == 200
    response = client.post("/category/", json={"name": "cat3"})
    assert response.status_code == 200
    """
    get all categories
    """
    # default
    response = client.get("/category/")
    assert response.status_code == 200
    assert len(response.json()) == 3

    # check skip
    response = client.get("/category/?skip=1")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "cat2"

    # check limit
    response = client.get("/category/?limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "cat3"


@pytest_db
def test_create_series():
    """
    create series
    """
    response = client.post("/series/", json={"name": "ser1"})
    assert response.status_code == 200


@pytest_db
def test_get_series():
    """
    create series
    """
    response = client.post("/series/", json={"name": "ser1"})
    assert response.status_code == 200
    response = client.post("/series/", json={"name": "ser2"})
    assert response.status_code == 200
    response = client.post("/series/", json={"name": "ser3"})
    assert response.status_code == 200
    """
    get all series
    """
    # default
    response = client.get("/series/")
    assert response.status_code == 200
    assert len(response.json()) == 3

    # check skip
    response = client.get("/series/?skip=1")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "ser2"

    # check limit
    response = client.get("/series/?limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "ser3"


@pytest_db
def test_create_tag():
    """
    create tag
    """
    response = client.post("/tag/", json={"name": "tag1"})
    assert response.status_code == 200


@pytest_db
def test_get_tag():
    """
    create tag
    """
    response = client.post("/tag/", json={"name": "tag1"})
    assert response.status_code == 200
    response = client.post("/tag/", json={"name": "tag2"})
    assert response.status_code == 200
    response = client.post("/tag/", json={"name": "tag3"})
    assert response.status_code == 200
    """
    get all tag
    """
    # default
    response = client.get("/tag/")
    assert response.status_code == 200
    assert len(response.json()) == 3

    # check skip
    response = client.get("/tag/?skip=1")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "tag2"

    # check limit
    response = client.get("/tag/?limit=2")
    assert response.status_code == 200
    assert len(response.json()) == 2
    assert response.json()[0]["name"] == "tag3"


def test_get_tags(SessionLocal):
    db = SessionLocal()

    crud.create_tag(db, schemas.CreateTag(**{'name': 'tag1'}))
    crud.create_tag(db, schemas.CreateTag(**{'name': 'tag2'}))
    crud.create_tag(db, schemas.CreateTag(**{'name': 'tag3'}))

    res = crud.get_tags(db, [1, 2])
    assert len(res) == 2

    try:
        exception = False
        crud.get_tags(db, [4])
    except KeyError:
        exception = True
    assert exception, 'Get Error tag id is invalid'

    db.close()
