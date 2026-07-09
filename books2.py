#Advanced concepts in FastAPI
# Data Validation, Exception handling, Status codes, Swagger Configuration, Python Request Objects

from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel, Field #pydantics - library for data validation, data modelling, data parsing, error handling

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    #constuctor to initialize book object

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating



class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3) #extra field validation using pydantic's Field class
    author: str = Field(min_length=1 )
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)


#pydantic configurations set the default values for the fields
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Journey to Senior Software Engineer",
                "author": "Risper",
                "description": "A book about advancing in software engineering",
                "rating": 5 
            }
        }
    }


BOOKS = [

    Book(1, "Journey to Senior Software Engineer", "Risper", "A book about advancing in software engineering", 5),
    Book(2, "Becoming a Fullstack Engineer", "Risper", "A comprehensive guide to becoming a fullstack engineer", 5),
    Book(3, "Master System Design", "Risper", "A book about mastering system design", 5),
    Book(4, "Frontend A-Z", "Risper", "A comprehensive guide to frontend development", 5),
    Book(5, "Hello Architect", "Risper", "A book about software architecture principles", 5)

]

@app.get("/books")
def read_all_boks():
    return BOOKS


@app.post("/create_book")
def create_book(book_request:BookRequest):
   
    new_book = Book(**book_request.model_dump()) #converting the request body to a Book object using the model_dump method
   
    BOOKS.append(find_book_id(new_book)) #finding the book id and appending the new book to the BOOKS list


def find_book_id(book: Book):
    # if len(BOOKS) > 0:
    #     book.id = BOOKS[-1].id + 1
    # else:
    #     book.id = 1
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1

    return book
