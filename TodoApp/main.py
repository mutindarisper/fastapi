from fastapi import FastAPI
import models
from models import Todos
from database import engine
from routers import auth, todos

app = FastAPI()

#takes everything from database.py and models.py to create a new database 
# that has a new table of todos with all the columns in models.py file
models.Base.metadata.create_all(bind=engine) 
app.include_router(auth.router) #include the auth router in the main app
app.include_router(todos.router) #include the todos router in the main app

