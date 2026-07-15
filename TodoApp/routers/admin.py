from fastapi import APIRouter, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Annotated
from models import Todos
from database import SessionLocal
from .auth import get_current_user


router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

#takes everything from database.py and models.py to create a new database 
# that has a new table of todos with all the columns in models.py file
# models.Base.metadata.create_all(bind=engine) 
# router.include_router(auth.router) #include the auth router in the main router

def get_db():
    db = SessionLocal() #contact the database and create a session
    try:
        yield db #return the info
    finally:
        db.close() #close the session after the data is returned

db_dependency =  Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)] #get the current user from the token


@router.get("/todos", status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependency, db: db_dependency): #dependency injection
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    
    return db.query(Todos).all() #query the db of all the Todos

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT) #delete a todo by id
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)): #dependency injection - this depends on the get_db function to get the db session
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first() #get the todo by id
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    db.query(Todos).filter(Todos.id == todo_id).delete() #delete the todo by id
    db.commit() #commit the changes to the db