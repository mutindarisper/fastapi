from fastapi import FastAPI, Depends, HTTPException, Path, status
from sqlalchemy.orm import Session
from typing import Annotated
import models
from models import Todos
from database import SessionLocal, engine

app = FastAPI()

#takes everything from database.py and models.py to create a new database 
# that has a new table of todos with all the columns in models.py file
models.Base.metadata.create_all(bind=engine) 

def get_db():
    db = SessionLocal() #contact the database and create a session
    try:
        yield db #return the info
    finally:
        db.close() #close the session after the data is returned

db_dependency =  Annotated[Session, Depends(get_db)]

@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency): #dependency injection - this depends on the get_db function to get the db session
    return db.query(Todos).all() #query the db of all the Todos


@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK) #get a specific todo by id
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first() #for performance, we use first() instead of all() to get the first result that matches the filter
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found") #if the todo is not found, return a 404 error