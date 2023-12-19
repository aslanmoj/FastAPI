from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
# from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from .routers import post, user, auth
from .config import settings

# models.Base.metadata.create_all(bind = engine)

app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)



# class Post(BaseModel):
#     title: str
#     content: str
#     published: bool=True

while True:
    try:
        conn = psycopg2.connect(host = 'localhost', database='fastapi', user = 'postgres'
                                , password='password', cursor_factory = RealDictCursor)
        
        cursor = conn.cursor()
        print('database connection was successful')
        break

    except Exception as error:
        print('Connecting to database has failed')
        print("Error: ",error)
        time.sleep(5)

my_posts=[{"title":"title of post1",
           "content":"content of post1",
           "id": 1},{
           "title":"Fav foods",
           "content":"I love pizza",
           "id":2}]
########################################################
# root
@app.get("/")
def read_root():
    return {"Hello": "to Aslan API"}



### Old Code, directly connects to db and not using SQL alchemy
########################################################
# Delete
@app.delete("/posts/{id}", status_code= status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    to_be_deleted = find_post(id)
    cursor.execute("""DELETE FROM posts WHERE id = (%s)
                   returning *""", (str(id),))
    to_be_deleted = cursor.fetchone()
    conn.commit()
    if not to_be_deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with ID: {id} was not found")
    print(to_be_deleted)
    # return {"delete_detail": f"post with id {id} was deleted"}
    return Response(status_code= status.HTTP_204_NO_CONTENT)
########################################################
# Update
@app.put("/posts/{id}")
def update_post (id:int, post: schemas.PostCreate):
    # index = find_index(id)
    cursor.execute("""UPDATE posts SET title = %s, content = %s,published = %s
                   WHERE id = %s
                   returning *"""
                   ,(post.title, post.content, post.published, str(id),))
    post = cursor.fetchone()
    conn.commit()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with ID: {id} was not found")
    

    print(post)
    return {'message': post}
########################################################
# Get post
@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    # one_post = find_post(id)
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    one_post = cursor.fetchone()

    if not one_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with ID: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'Message': f"post with ID {id} was not found"}
    print(one_post)

    return {"post_detail": one_post}
########################################################
# get all
@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print (posts)
    return {"data": posts}
########################################################
# post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: schemas.PostBase):
    cursor.execute("""INSERT INTO posts (title, content, published)
                   VALUES(%s,%s,%s)
                   returning *""",(new_post.title, new_post.content
                                        , new_post.published))
    posts = cursor.fetchone()
    conn.commit()
    print (posts)
    return {"data": posts}
########################################################
# Aux funcs
def find_post(id):
    for dic in my_posts:
        if(dic['id'] == id):
            return dic

def find_index(id):
    for idx,dic in enumerate(my_posts):
        if(dic['id'] == id):
            return idx