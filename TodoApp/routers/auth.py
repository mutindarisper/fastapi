from typing import Annotated

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter() #use router instead of app so that we can use it as a route in the main app
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto') #hashing the password using bcrypt


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3)
    email: str = Field(min_length=3)
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    password: str = Field(min_length=3)
    role: str = Field(min_length=3)


def get_db():
    db = SessionLocal() #contact the database and create a session
    try:
        yield db #return the info
    finally:
        db.close() #close the session after the data is returned

db_dependency =  Annotated[Session, Depends(get_db)]

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return True
    
   

@router.post("/auth", status_code=status.HTTP_201_CREATED) #create a new user
async def create_user(db: db_dependency, create_user_request: CreateUserRequest):

    create_user_request_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password), #in a real app, you would hash the password before storing it
        is_active=True,
        role=create_user_request.role

    )
    #save the new user to the database
    db.add(create_user_request_model) #add the new user to the db session
    db.commit() #commit the changes to the db
    #return create_user_request_model

@router.post("/token")
async def login_for_access_token(form_data:Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        return "Failed Authentication"
    return 'Succesful Authentication'
