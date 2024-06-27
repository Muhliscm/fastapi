from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schema, oauth2

router = APIRouter(
    prefix='/votes',
    tags=['votes']
)


@router.post('/', status_code=status.HTTP_201_CREATED)
def like_post(vote: schema.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {vote.post_id} not found")

    query_vote = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)

    found_vote = query_vote.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"post already liked by {current_user.id}")

        new_vote = models.Vote(user_id=current_user.id, post_id=vote.post_id)
        db.add(new_vote)
        db.commit()
        return {"message": "post liked success"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id {vote.post_id} not liked")
        query_vote.delete()
        db.commit()
        return {"message": "successfully disliked the post"}
