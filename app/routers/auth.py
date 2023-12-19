from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm



router = APIRouter(tags = ['Authentication'])



@router.post('/login', response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(),db: Session = Depends(get_db)):
    #user = db.query(models.User).filter(models.User.email == user_credentials.email).first() # this is used if we use models schema
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() # this is for Oauth2PasswordRequestForm
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail= "Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail= "Invalid Credentials")
    
    # Create Token
    # Return Token
    acces_token = oauth2.create_Access_token(data={"user_id":user.id})
    return {"access_token": acces_token, "token_type":"bearer"}