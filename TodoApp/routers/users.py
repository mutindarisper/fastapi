from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Annotated
from models import Users
from database import SessionLocal
from .auth import get_current_user
from passlib.context import CryptContext



router = APIRouter(
    prefix="/users",
    tags=["users"],
)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto') #hashing the password using bcrypt


def get_db():
    db = SessionLocal() #contact the database and create a session
    try:
        yield db #return the info
    finally:
        db.close() #close the session after the data is returned

db_dependency =  Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)] #get the current user from the token


class UserVerificationRequest(BaseModel):
    password: str 
    new_password: str = Field(min_length=6)


@router.get("/", status_code=status.HTTP_200_OK)
def get_users(db: db_dependency, user: user_dependency):
    #return all info about a user
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    users = db.query(Users).filter(Users.id == user.get("id")).first() #get all info for a specific user by id
    return users


@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
def update_user_password(user:user_dependency,  db: db_dependency, user_verification: UserVerificationRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    user_model = db.query(Users).filter(Users.id == user.get("id")).first()

    #verify if current password matches the hashed password in the database before updating to a new password
    if not bcrypt_context.verify(user_verification.password, user_model.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error on password change")
    
    user_model.hashed_password = bcrypt_context.hash(user_verification.new_password)
    db.add(user_model)
    db.commit()
    

