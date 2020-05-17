from starlette.testclient import TestClient
from app.main import app
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
def test_create_post():
    """
    create post
    """
    user = client.post(
        "/users/", json={"email": "foo", "username": "fooo", "password": "fo"}
    )
    assert user.status_code == 200
    category = client.post("/category/", json={"name": "cat"})
    assert category.status_code == 200
    series = client.post("/series/", json={"name": "ser"})
    assert series.status_code == 200
    tag = client.post("/tag/", json={"name": "tag"})
    assert tag.status_code == 200

    response = client.post(
        "/post/",
        json={
            "title": "1",
            "body": "1",
            "public_at": "2020-05-17T00:00:00",
            "category": category.json()["name"],
            "series": series.json()["name"],
            "tags": [tag.json()["name"]],
        },
    )
    assert response.status_code == 200


@pytest_db
def test_get_post():
    """
    get post
    """
    user = client.post(
        "/users/", json={"email": "foo", "username": "fooo", "password": "fo"}
    )
    assert user.status_code == 200
    category = client.post("/category/", json={"name": "cat"})
    category_name = category.json()["name"]
    assert category.status_code == 200
    series = client.post("/series/", json={"name": "ser"})
    series_name = series.json()["name"]
    assert series.status_code == 200
    tag = client.post("/tag/", json={"name": "tag"})
    tag_name = tag.json()["name"]
    assert tag.status_code == 200

    response = client.post(
        "/post/", json={"title": "1", "body": "1", "category": category_name, "public_at": "2020-05-17T00:00:00", },
    )
    assert response.status_code == 200
    response = client.post(
        "/post/", json={"title": "2", "body": "2", "series": series_name, "public_at": "2020-05-17T00:00:00", },
    )
    assert response.status_code == 200
    response = client.post(
        "/post/", json={"title": "3", "body": "3", "tags": [tag_name], "is_public": True, "public_at": "2020-05-17T00:00:00", },
    )
    assert response.status_code == 200

    """
    get all posts
    """
    # default
    response = client.get("/post/")
    assert response.status_code == 200
    assert len(response.json()['data']) == 3
    assert response.json()['max_page'] == 1

    # check page 1
    response = client.get("/post/?page=1&length=2")
    assert response.status_code == 200
    assert len(response.json()['data']) == 2
    assert response.json()['data'][0]["title"] == "3"
    assert response.json()['max_page'] == 2

    # check page 2
    response = client.get("/post/?page=2&length=2")
    assert response.status_code == 200
    assert len(response.json()['data']) == 1
    assert response.json()['data'][0]["title"] == "1"
    assert response.json()['max_page'] == 2

    """filter"""
    # category
    response = client.get(f"/post/?category={category_name}")
    assert response.status_code == 200
    assert len(response.json()['data']) == 1

    # series
    response = client.get(f"/post/?series={series_name}")
    assert response.status_code == 200
    assert len(response.json()['data']) == 1

    # tag
    response = client.get(f"/post/?tags={tag_name}")
    assert response.status_code == 200
    assert len(response.json()['data']) == 1

    # is_public
    response = client.get(f"/post/?is_private=False")
    assert response.status_code == 200
    assert len(response.json()['data']) == 1


@pytest_db
def test_get_post_by_id():
    """
    get post by id
    """
    user = client.post(
        "/users/", json={"email": "foo", "username": "fooo", "password": "fo"}
    )
    assert user.status_code == 200

    response = client.post("/post/", json={"title": "1", "body": "1", "public_at": "2020-05-17T00:00:00", })
    assert response.status_code == 200

    response = client.post("/post/", json={"title": "2", "body": "2", "public_at": "2020-05-17T00:00:00", })
    assert response.status_code == 200

    response = client.get("/post/2/")
    assert response.status_code == 200
    assert response.json()["title"] == "2"


@pytest_db
def test_delete_post():
    """
    delete post
    """
    user = client.post(
        "/users/", json={"email": "foo", "username": "fooo", "password": "fo"}
    )
    assert user.status_code == 200
    category = client.post("/category/", json={"name": "cat"})
    assert category.status_code == 200
    series = client.post("/series/", json={"name": "ser"})
    assert series.status_code == 200
    tag = client.post("/tag/", json={"name": "tag"})
    assert tag.status_code == 200

    response = client.post(
        "/post/",
        json={
            "title": "1",
            "body": "1",
            "public_at": "2020-05-17T00:00:00", 
            "category": category.json()["name"],
            "series": series.json()["name"],
            "tags": [tag.json()["name"]],
        },
    )
    assert response.status_code == 200

    response = client.delete(f"/post/{1}/")
    assert response.status_code == 200

    response = client.get("/post/")
    assert response.status_code == 400


@pytest_db
def test_create_comment():
    """
    create comment
    """
    user = client.post(
        "/users/", json={"email": "foo", "username": "fooo", "password": "fo"}
    )
    assert user.status_code == 200
    user_id = user.json()["id"]

    response = client.post("/post/", json={"title": "1", "body": "1", "public_at": "2020-05-17T00:00:00", })
    assert response.status_code == 200

    post_id = response.json()["id"]
    response = client.post("/comment/", json={"body": "hogefuga", "post_id": post_id, })
    assert response.status_code == 200


@pytest_db
def test_get_comment():
    """
    get comment
    """
    user = client.post(
        "/users/", json={"email": "foo", "username": "fooo", "password": "fo"}
    )
    assert user.status_code == 200
    user_id = user.json()["id"]

    response = client.post("/post/", json={"title": "1", "body": "1", "public_at": "2020-05-17T00:00:00", })
    assert response.status_code == 200

    post_id = response.json()["id"]
    response = client.post("/comment/", json={"body": "hogefuga", "post_id": post_id})
    assert response.status_code == 200

    response = client.get(f"/comment/{post_id}")
    assert response.status_code == 200
    assert len(response.json()) == 1


@pytest_db
def test_delete_comment():
    """
    delete comment
    """
    user = client.post(
        "/users/", json={"email": "foo", "username": "fooo", "password": "fo"}
    )
    assert user.status_code == 200
    user_id = user.json()["id"]

    response = client.post("/post/", json={"title": "1", "body": "1", "public_at": "2020-05-17T00:00:00", })
    assert response.status_code == 200

    post_id = response.json()["id"]
    response = client.post("/comment/", json={"body": "hogefuga", "post_id": post_id})
    assert response.status_code == 200
    comment_id = response.json()["id"]

    response = client.delete(f"/comment/{comment_id}/")
    assert response.status_code == 200

    response = client.get(f"/comment/{post_id}")
    assert response.status_code == 400
