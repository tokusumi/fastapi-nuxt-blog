from typing import List, Optional
from fastapi import Depends, APIRouter, HTTPException, Query
from sqlalchemy.orm import Session
from . import models, schemas, crud, utils
from settings.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = APIRouter()


@app.get("/post/", response_model=List[schemas.Post], tags=['post'])
def get_post(
        author: Optional[str] = None,
        category: Optional[str] = None,
        series: Optional[str] = None,
        tags: Optional[List[str]] = Query(None),
        skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    filtering = schemas.FilterPost(author=author, category=category, series=series, tags=tags)
    filtering_dict = utils.FilterIDPost(db, filtering).to_items() if filtering else {}
    query = crud.get_post_query(db, skip=skip, limit=limit, **filtering_dict)
    if len(query) == 0:
        raise HTTPException(status_code=400, detail="Post does not exist")
    return query


@app.get("/post/{post_id}/", response_model=schemas.Post, tags=['post'])
def get_post_by_id(post_id: int, db: Session = Depends(get_db)):
    query = crud.get_post(db, post_id)
    if not query:
        raise HTTPException(status_code=400, detail="Post does not exist")
    return query


@app.post("/post/", response_model=schemas.Post, tags=['post'])
def create_post(post: schemas.CreatePostReq, db: Session = Depends(get_db)):
    create_id_post_dict = utils.CreateIDPost(db, post).to_items()
    _post = schemas.CreatePost(**create_id_post_dict)
    return crud.create_post(db, _post)


@app.delete("/post/", response_model=schemas.Success, tags=['post'])
def delete_post(post: schemas.DeletePost, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post.id)
    if not db_post:
        raise HTTPException(status_code=400, detail="Does not exist")
    crud.delete_post(db, post.id)
