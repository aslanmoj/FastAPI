
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from .. import models, schemas, utils
from sqlalchemy.orm import Session
from ..database import engine, SessionLocal, get_db
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor


router = APIRouter(tags = ['users'])



########################################################
# post Using SQL Alchemy
@router.post("/users", status_code=status.HTTP_201_CREATED,response_model= schemas.UserOut)
def create_CreateUser(users: schemas.UserCreate,db: Session = Depends(get_db)):


    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    new_user = models.User(**users.dict())
    new_user.password = utils.hash(new_user.password)
    print(new_user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

########################################################
# Get One post SQLAlchemy
@router.get("/users/{id}", response_model=schemas.UserOut)
def get_user(id: int, response: Response, db: Session = Depends(get_db)):
    # one_post = find_post(id)
    one_user = db.query(models.User).filter(models.User.id == id).first()
    # print(one_post)
    if not one_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"user with ID: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'Message': f"post with ID {id} was not found"}
    print(one_user)

    return one_user