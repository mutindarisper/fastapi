#sqlalchemy code
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:%40test3R7376!@localhost/TodoApplicationDatabase' #creates the location of the db of our app

engine = create_engine(SQLALCHEMY_DATABASE_URL) 

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine) #creates a session for the db

Base = declarative_base() #later on call db create base which controls the db, creaTE TABLES ETC