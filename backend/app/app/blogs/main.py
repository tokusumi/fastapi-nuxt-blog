from typing import List, Optional
from fastapi import Depends, APIRouter, HTTPException, Query
from sqlalchemy.orm import Session
from app.blogs import models, schemas, crud, utils
from app.db.session import get_db
from app.auth.authentications import get_current_active_user
from app.notifications.notify import post_mail_notify

app = APIRouter()


@app.get("/post/", response_model=schemas.Posts, tags=["post"])
def get_post(
    author: Optional[str] = None,
    category: Optional[str] = None,
    series: Optional[str] = None,
    tags: Optional[List[str]] = Query(None),
    is_private: Optional[bool] = True,
    page: int = Query(1, gt=0),
    length: int = Query(6, gt=0),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    skip = length * (page - 1)
    limit = length
    filtering = schemas.FilterPost(
        author=author,
        category=category,
        series=series,
        tags=tags,
        is_private=is_private,
    )
    filtering_dict = utils.FilterIDPost(db, filtering).to_items() if filtering else {}
    query, max_page, total = crud.get_post_query(
        db, skip=skip, limit=limit, is_private=filtering.is_private, **filtering_dict
    )
    if len(query) == 0:
        raise HTTPException(status_code=400, detail="Post does not exist")
    return {"data": query, "max_page": max_page, "total": total}


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

    obj = crud.create_post(db, _post)

    if obj.notification and obj.is_public:
        post_mail_notify(obj)

    return obj


@app.put("/post/{post_id}/", response_model=schemas.Post, tags=["post"])
def update_post(
    post_id: int,
    post: schemas.UpdatePostReq,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_active_user),
):
    _post = crud.get_post(db, post_id)
    if _post.author_id != current_user.id:
        raise HTTPException(status_code=400, detail="must be modified by author")
    update_postID = utils.UpdateIDPost(db, post)
    if len(update_postID.to_items()) == 0:
        raise HTTPException(status_code=400, detail="no context")

    obj = crud.update_post(db, _post, update_postID)

    if obj.notification and obj.is_public:
        post_mail_notify(obj)

    return obj


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
    skip: int = Query(0, gt=-1),
    limit: int = Query(100, gt=0),
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
    if comment.body == "":
        raise HTTPException(status_code=400, detail="No Comment")
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
