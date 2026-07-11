from fastapi import FastAPI, Depends, HTTPException, Path, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from typing import Annotated
import models
from models import Todos
from database import SessionLocal, engine
from routers import auth

app = FastAPI()

#takes everything from database.py and models.py to create a new database 
# that has a new table of todos with all the columns in models.py file
models.Base.metadata.create_all(bind=engine) 
app.include_router(auth.router) #include the auth router in the main app

def get_db():
    db = SessionLocal() #contact the database and create a session
    try:
        yield db #return the info
    finally:
        db.close() #close the session after the data is returned

db_dependency =  Annotated[Session, Depends(get_db)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool

@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency): #dependency injection - this depends on the get_db function to get the db session
    return db.query(Todos).all() #query the db of all the Todos


@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK) #get a specific todo by id
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first() #for performance, we use first() instead of all() to get the first result that matches the filter
    if todo_model is not None:
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not found") #if the todo is not found, return a 404 error




@app.post("/todo", status_code=status.HTTP_201_CREATED) #create a new todo
async def create_todo(todo_request: TodoRequest, db: db_dependency):
    todo_model = Todos(**todo_request.model_dump()) #convert the request body to a Todos object using the model_dump method
    db.add(todo_model) #about to add the new todo to the db session
    db.commit() #commit the changes to the db
  

@app.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT) #update a todo by id
async def update_todo(db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
   
   todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
   if todo_model is None:
       raise HTTPException(status_code = 404, detail="Todo not found")
   todo_model.title = todo_request.title
   todo_model.description = todo_request.description
   todo_model.priority = todo_request.priority
   todo_model.complete = todo_request.complete

   db.add(todo_model)
   db.commit()


@app.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(db: db_dependency, todo_id: int = Path(gt=0)):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()