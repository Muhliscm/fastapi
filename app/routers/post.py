
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from .. import models, schema, oauth2
from sqlalchemy import func


router = APIRouter(
    prefix='/posts',
    tags=['posts']
)


@router.get('/', response_model=List[schema.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(
        models.Post.content.contains(search)).limit(limit).offset(skip).all()

    return results


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schema.Post)
def create_posts(post: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),):
    # post_dict = post.model_dump()
    # post_dict['id'] = randrange(1, 20000)
    # my_posts.routerend(post_dict)

    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", response_model=schema.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(
            status_code=404, detail=f"Post with id {id} not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} not found!")

    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="No permission to perform this action")

    post_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schema.Post)
def update_post(id: int, post_model: schema.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(404, detail=f"post with id: {id} not found!")

    if post.owner_id != current_user.id:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
                            detail="No permission to perform this action")

    post_query.update(post_model.model_dump(), synchronize_session=False)
    db.commit()

    return post_query.first()
