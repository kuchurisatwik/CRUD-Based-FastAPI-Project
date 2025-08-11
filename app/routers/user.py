from .. import models,schemas,utils
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter 
from sqlalchemy.orm import Session
from ..DataBase import get_db
from typing import List
from sqlalchemy.exc import IntegrityError


router = APIRouter(
    prefix = "/users",
    tags = ['Users']
)

@router.get("/",response_model = List[schemas.ResUser])
def get_users(db: Session = Depends(get_db)):
    data = db.query(models.User).all()
    return data

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ResUser)
def create_user(user: schemas.Users, db: Session = Depends(get_db)):

    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user



@router.get("/{id}",response_model = schemas.ResUser)
def get_user(id: int,db: Session = Depends(get_db)):
    data = db.query(models.User).filter(models.User.id == id).first()
    if data == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"post with id: {id} was not found")
    return data


@router.put("/{id}",response_model = schemas.ResUser)
def update_user(id: int , up_user : schemas.Users ,db:Session = Depends(get_db)):
    data_query = db.query(models.User).filter(models.User.id == id)
    data = data_query.first()
    if data == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail= f"The user with id: {id} does not exist")
    data_query.update(up_user.dict(), synchronize_session = False)
    db.commit()
    return data_query.first()



@router.delete("/{id}")
def del_users(id: int, db:Session = Depends(get_db)):
    data_query = db.query(models.User).filter(models.User.id == id).first()
    if data_query == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,
                            detail = f"The user with id: {id} does'nt exist")
        
    data_query.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)
    
