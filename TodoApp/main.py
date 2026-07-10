from fastapi import FastAPI

import models
from database import engine

app = FastAPI()

#takes everything from database.py and models.py to create a new database 
# that has a new table of todos with all the columns in models.py file
models.Base.metadata.create_all(bind=engine) 