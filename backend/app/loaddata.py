import json
import argparse
from datetime import datetime
from app.db.session import SessionLocal
from app.db.load_base import Base
from app.db.load_base import User, Category, Tag, Series, Post, Comment


def get_data(path: str):
    with open(path, "r", encoding="utf-8") as f:
        json_dict = json.load(f)
    return json_dict


def serialize(data):
    out = {}
    for field in data:
        if field.get('model') not in out:
            out[field.get('model')] = {}
        out[field.get('model')][field.get('pk')] = field.get('fields')
    return out


def iso_to_dt(iso):
    try:
        return datetime.strptime(iso, '%Y-%m-%dT%H:%M:%S.%fZ')
    except ValueError:
        return datetime.strptime(iso, '%Y-%m-%dT%H:%M:%SZ')


def load_user(data):
    db = SessionLocal()
    try:

        model_name = "accounts.myuser"
        users = [
            {
                'id': pk, 'username': v['username'], 'email': v['email'],
                'icon': v['avatar'], 'hashed_password': v['password']
            }
            for pk, v in data.get(model_name).items()]
        db.execute(User.__table__.insert(), users)
        db.commit()
        db.close()
    except:
        db.close()


def load_subprops(data):
    db = SessionLocal()
    try:
        model_name = 'blogs.category'
        categories = [{'id': pk, 'name': v['name'], 'created_at': iso_to_dt(v['created_at'])}
                      for pk, v in data.get(model_name).items()]
        db.execute(Category.__table__.insert(), categories)
        db.commit()

        model_name = 'blogs.series'
        categories = [{'id': pk, 'name': v['name'], 'created_at': iso_to_dt(v['created_at'])}
                      for pk, v in data.get(model_name).items()]
        db.execute(Series.__table__.insert(), categories)
        db.commit()

        model_name = 'blogs.tag'
        categories = [{'id': pk, 'name': v['name'], 'created_at': iso_to_dt(v['created_at'])}
                      for pk, v in data.get(model_name).items()]
        db.execute(Tag.__table__.insert(), categories)
        db.commit()

        db.close()
    except:
        db.close()


def load_post(data):
    db = SessionLocal()
    try:
        model_name = 'blogs.post'
        posts = [
            {
                'id': pk,
                'title': v['title'],
                'author_id': v['author'],
                'image': v['image'],
                'category_id': v['category'],
                'series_id': v['series'],
                'created_at': iso_to_dt(v['created_at']),
                'public_at': iso_to_dt(v['updated_at']),
                "body": v['body'],
                'is_public': v['is_public'],
                'notification': v['notification'],

            } for pk, v in data.get(model_name).items()
        ]
        db.execute(Post.__table__.insert(), posts)
        db.commit()
    except:
        pass


def load_comment(data):
    db = SessionLocal()
    try:
        model_name = 'blogs.comment'
        categories = [{'id': pk, 'author_id': v['author'], 'post_id': v['post'], "body": v['body'], 'created_at': iso_to_dt(v['created_at'])}
                      for pk, v in data.get(model_name).items()]
        db.execute(Comment.__table__.insert(), categories)
        db.commit()
    except:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--path', default='dumped.json')
    args = parser.parse_args()

    data = get_data(args.path)
    data = serialize(data)

    load_user(data)
    load_subprops(data)

    load_post(data)
    load_comment(data)
