from fastapi import FastAPI, Depends
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

@app.get("/")
async def read_all(db: db_dependency): #dependency injection - this depends on the get_db function to get the db session
    return db.query(Todos).all()