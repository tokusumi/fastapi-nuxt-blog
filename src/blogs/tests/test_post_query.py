from blogs import models, crud, schemas
from users import crud as u_crud, schemas as u_schemas


def test_create_post(SessionLocal):
    db = SessionLocal()
    user = u_crud.create_user_query(db, u_schemas.UserCreate(**{"email": "foo", "name": "fooo", "password": "fo"}))
    category = crud.create_category(db, schemas.CreateCategory(**{"name": 'cat'}))
    series = crud.create_series(db, schemas.CreateSeries(**{"name": 'ser'}))
    tag = crud.create_tag(db, schemas.CreateTag(**{"name": 'tag'}))

    posts = {
        'title': 'hoge',
        'body': 'fuga',
        'author_id': user.id,
        'category_id': category.id,
        'series_id': series.id,
        'tag_ids': [tag.id],
    }
    post = crud.create_post(db, schemas.CreatePost(**posts))
    assert post.title == 'hoge'
    assert post.body == 'fuga'
    assert post.author_id == user.id
    assert post.category_id == category.id
    assert post.series_id == series.id
    assert post.tag[0] == tag
    db.close()


def test_delete_post(SessionLocal):
    db = SessionLocal()
    user = u_crud.create_user_query(db, u_schemas.UserCreate(**{"email": "foo", "name": "fooo", "password": "fo"}))
    category = crud.create_category(db, schemas.CreateCategory(**{"name": 'cat'}))
    series = crud.create_series(db, schemas.CreateSeries(**{"name": 'ser'}))
    tag = crud.create_tag(db, schemas.CreateTag(**{"name": 'tag'}))
    tag_name = tag.name

    posts = {
        'title': 'hoge',
        'body': 'fuga',
        'author_id': user.id,
        'category_id': category.id,
        'series_id': series.id,
        'tag_ids': [tag.id],
    }
    post = crud.create_post(db, schemas.CreatePost(**posts))
    db.close()

    db = SessionLocal()
    crud.delete_post(db, post.id)
    db.close()

    db = SessionLocal()
    post = crud.get_post(db, post.id)
    assert post is None
    db.close()

    db = SessionLocal()
    _tag = crud.get_tag(db, tag_name)
    assert _tag.name == tag_name, 'tag is deleted'
    db.close()


def test_filter_by_category(SessionLocal):
    db = SessionLocal()
    user = u_crud.create_user_query(db, u_schemas.UserCreate(**{"email": "foo", "name": "fooo", "password": "fo"}))
    category = crud.create_category(db, schemas.CreateCategory(**{"name": 'cat'}))

    posts = {
        'title': 'hoge',
        'body': 'fuga',
        'author_id': user.id,
        'category_id': category.id,
    }
    crud.create_post(db, schemas.CreatePost(**posts))

    q = db.query(models.Post)
    q = crud.filter_post_by_category(q, category.id)
    assert len(q.all()) == 1
    q = db.query(models.Post)
    q = crud.filter_post_by_category(q, category.id + 1)
    assert len(q.all()) == 0, 'filtering by category does not work'
    db.close()


def test_filter_by_series(SessionLocal):
    db = SessionLocal()
    user = u_crud.create_user_query(db, u_schemas.UserCreate(**{"email": "foo", "name": "fooo", "password": "fo"}))
    series = crud.create_series(db, schemas.CreateSeries(**{"name": 'ser'}))

    posts = {
        'title': 'hoge',
        'body': 'fuga',
        'author_id': user.id,
        'series_id': series.id,
    }
    crud.create_post(db, schemas.CreatePost(**posts))

    q = db.query(models.Post)
    q = crud.filter_post_by_series(q, series.id)
    assert len(q.all()) == 1
    q = db.query(models.Post)
    q = crud.filter_post_by_series(q, series.id + 1)
    assert len(q.all()) == 0, 'filtering by category does not work'
    db.close()


def test_filter_by_tag(SessionLocal):
    db = SessionLocal()
    user = u_crud.create_user_query(db, u_schemas.UserCreate(**{"email": "foo", "name": "fooo", "password": "fo"}))
    tag = crud.create_tag(db, schemas.CreateTag(**{"name": 'tag'}))

    posts = {
        'title': 'hoge',
        'body': 'fuga',
        'author_id': user.id,
        'tag_ids': [tag.id],
    }
    crud.create_post(db, schemas.CreatePost(**posts))

    q = db.query(models.Post)
    q = crud.filter_post_by_tag(q, tag.id)
    assert len(q.all()) == 1
    q = db.query(models.Post)
    q = crud.filter_post_by_tag(q, tag.id + 1)
    assert len(q.all()) == 0, 'filtering by category does not work'
    db.close()


def test_filter_by_tags(SessionLocal):
    db = SessionLocal()
    user = u_crud.create_user_query(db, u_schemas.UserCreate(**{"email": "foo", "name": "fooo", "password": "fo"}))
    tag1 = crud.create_tag(db, schemas.CreateTag(**{"name": 'tag1'}))
    tag2 = crud.create_tag(db, schemas.CreateTag(**{"name": 'tag2'}))

    posts = {
        'title': 'hoge',
        'body': 'fuga',
        'author_id': user.id,
        'tag_ids': [tag1.id],
    }
    crud.create_post(db, schemas.CreatePost(**posts))

    posts = {
        'title': 'hoge',
        'body': 'fuga',
        'author_id': user.id,
        'tag_ids': [tag1.id, tag2.id],
    }
    crud.create_post(db, schemas.CreatePost(**posts))

    q = db.query(models.Post)
    q = crud.filter_post_by_tags(q, [tag1.id, tag2.id])
    assert len(q.all()) == 1
    db.close()


def test_filter_by_is_public(SessionLocal):
    db = SessionLocal()
    user = u_crud.create_user_query(db, u_schemas.UserCreate(**{"email": "foo", "name": "fooo", "password": "fo"}))

    posts = {
        'title': 'hoge',
        'body': 'fuga',
        'author_id': user.id,
        'is_public': False
    }
    crud.create_post(db, schemas.CreatePost(**posts))

    q = db.query(models.Post)
    q = crud.filter_post_by_is_public(q)
    assert len(q.all()) == 0
    db.close()
