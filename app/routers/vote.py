from .. import utils,DataBase,oauth2,schemas,models
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session


router = APIRouter(
    prefix = "/votes",
    tags = ['votes']
)


@router.post("/",status_code = status.HTTP_201_CREATED)
def vote(vote: schemas.Vote,db: Session = Depends(DataBase.get_db),
current_user: int = Depends(oauth2.get_current_user)):
    
    vote_query=db.query(models.Vote).filter(models.Vote.posts_id == vote.post_id,
                                models.Vote.users_id == current_user.id)
    found_vote = vote_query.first()
    if (vote.dir == 1):
        if found_vote:
            raise HTTPException(status_code= status.HTTP_409_CONFLICT,
                    detail = f"user{current_user,id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id,user_id = current_user.id)
        db.add(new_vote)
        db.commit()