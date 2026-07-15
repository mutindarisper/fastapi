from fastapi import APIRouter
from pydantic import BaseModel, Field

from models import Users
from passlib.context import CryptContext


router = APIRouter() #use router instead of app so that we can use it as a route in the main app
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto') #hashing the password using bcrypt


class CreateUserRequest(BaseModel):
    username: str = Field(min_length=3)
    email: str = Field(min_length=3)
    first_name: str = Field(min_length=3)
    last_name: str = Field(min_length=3)
    password: str = Field(min_length=3)
    role: str = Field(min_length=3)

@router.post("/auth")
async def create_user(create_user_request: CreateUserRequest):

    create_user_request_model = Users(
        username=create_user_request.username,
        email=create_user_request.email,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        hashed_password=bcrypt_context.hash(create_user_request.password), #in a real app, you would hash the password before storing it
        is_active=True,
        role=create_user_request.role

    )
    return create_user_request_model