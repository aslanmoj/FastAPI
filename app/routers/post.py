
from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.params import Body
from .. import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from typing import List,Optional
from ..database import engine, SessionLocal, get_db
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import func



router = APIRouter(prefix="/postsSQLAlchemy",
                   tags = ['posts'])

########################################################
# Get all with SQLAlchemy
@router.get("/")
def test_posts(db: Session = Depends(get_db), 
                 current_user:int = Depends(oauth2.get_current_User)
                ,limit: int =10, skip: int = 0, search: Optional[str]=""):
    posts = db.query(models.Post).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    results = db.query(models.Post, func.count(models.Post.id)).join(models.User, models.User.id == models.Post.owner_id
                                           , isouter = True ).group_by(models.Post.id).all()
    
    
    print(results)
    return{'data:': posts}

########################################################
# post Using SQL Alchemy
@router.post("/", status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostBase,db: Session = Depends(get_db), 
                 current_user:int = Depends(oauth2.get_current_User)):

    print(current_user.email)
    print(current_user.id)
    # new_post = models.Post(title = post.title, content = post.content, published = post.published)
    new_post = models.Post(owner_id = current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post
########################################################
# Get One post SQLAlchemy
@router.get("/{id}")
def get_post(id: int, response: Response, db: Session = Depends(get_db), 
                 current_user:int = Depends(oauth2.get_current_User)):
    # one_post = find_post(id)
    one_post = db.query(models.Post).filter(models.Post.id == id).first()
    # print(one_post)
    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with ID: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'Message': f"post with ID {id} was not found"}
    print(one_post)

    return {"post_detail": one_post}

########################################################
# Update using SQL Alchemy
@router.put("/{id}")
def update_post (id:int, post: schemas.PostCreate,db: Session = Depends(get_db),
                 current_user : int = Depends(oauth2.get_current_User)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    if post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with ID: {id} was not found")
    if post_query.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not Authorized to perform requested action")
    
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    print(post)
    return {'message': post_query.first()}
########################################################
# Delete using SQL Alchemy
@router.delete("/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db),
                current_user : int = Depends(oauth2.get_current_User)):
    to_be_deleted = db.query(models.Post).filter(models.Post.id == id)
    post = to_be_deleted.first()
    print (current_user.id)
    print(post.owner_id)
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with ID: {id} was not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail = "Not Authorized to perform requested action")
    

    to_be_deleted.delete(synchronize_session=False)   
    db.commit()   

    print(to_be_deleted)
    # return {"delete_detail": f"post with id {id} was deleted"}
    return Response(status_code= status.HTTP_204_NO_CONTENT)
