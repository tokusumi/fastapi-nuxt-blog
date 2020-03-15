from typing import List, Optional
from fastapi import Depends, APIRouter, HTTPException, Query
from sqlalchemy.orm import Session
from . import models, schemas, crud, utils
from settings.database import engine, get_db
from auth.authentications import get_current_active_user


models.Base.metadata.create_all(bind=engine)

app = APIRouter()


@app.get("/post/", response_model=List[schemas.Post], tags=["post"])
def get_post(
    author: Optional[str] = None,
    category: Optional[str] = None,
    series: Optional[str] = None,
    tags: Optional[List[str]] = Query(None),
    is_private: Optional[bool] = True,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    filtering = schemas.FilterPost(
        author=author, category=category, series=series, tags=tags, is_private=is_private
    )

    filtering_dict = utils.FilterIDPost(db, filtering).to_items() if filtering else {}
    query = crud.get_post_query(db, skip=skip, limit=limit, is_private=filtering.is_private, **filtering_dict)
    if len(query) == 0:
        raise HTTPException(status_code=400, detail="Post does not exist")
    return query


@app.get("/post/{post_id}/", response_model=schemas.Post, tags=["post"])
def get_post_by_id(
    post_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    query = crud.get_post(db, post_id)
    if not query:
        raise HTTPException(status_code=400, detail="Post does not exist")
    return query


@app.post("/post/", response_model=schemas.Post, tags=["post"])
def create_post(
    post: schemas.CreatePostReq,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    create_id_post_dict = utils.CreateIDPost(db, post).to_items()
    create_id_post_dict["author_id"] = current_user.id
    _post = schemas.CreatePost(**create_id_post_dict)
    return crud.create_post(db, _post)


@app.delete("/post/{post_id}/", response_model=schemas.Success, tags=["post"])
def delete_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    db_post = crud.get_post(db, post_id)
    if not db_post:
        raise HTTPException(status_code=400, detail="Does not exist")
    crud.delete_post(db, post_id)


@app.get("/comment/{post_id}/", response_model=List[schemas.Comment], tags=["comment"])
def get_comment_by_id(
    post_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    query = crud.get_comment_query(db, post_id, skip=skip, limit=limit)
    if len(query) == 0:
        raise HTTPException(status_code=400, detail="Comment does not exist")
    return query


@app.post("/comment/", response_model=schemas.Comment, tags=["comment"])
def create_comment(
    comment: schemas.CreateComment,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    return crud.create_comment(db, comment, author_id=current_user.id)


@app.delete("/comment/{comment_id}/", response_model=schemas.Success, tags=["comment"])
def delete_comment(
    comment_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    db_comment = crud.get_comment(db, comment_id)
    if not db_comment:
        raise HTTPException(status_code=400, detail="Does not exist")
    crud.delete_comment(db, comment_id)
