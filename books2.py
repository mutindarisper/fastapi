#Advanced concepts in FastAPI
# Data Validation, Exception handling, Status codes, Swagger Configuration, Python Request Objects

from typing import Optional

from fastapi import FastAPI, Path
from pydantic import BaseModel, Field #pydantics - library for data validation, data modelling, data parsing, error handling

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    #constuctor to initialize book object

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date



class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3) #extra field validation using pydantic's Field class
    author: str = Field(min_length=1 )
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)
    published_date: int = Field(gt=1997, lt=2027)


#pydantic configurations set the default values for the fields
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "Journey to Senior Software Engineer",
                "author": "Risper",
                "description": "A book about advancing in software engineering",
                "rating": 5,
                "published_date": 2012
            }
        }
    }


BOOKS = [

    Book(1, "Journey to Senior Software Engineer", "Risper", "A book about advancing in software engineering", 5, 2012),
    Book(2, "Becoming a Fullstack Engineer", "Risper", "A comprehensive guide to becoming a fullstack engineer", 5, 2014),
    Book(3, "Master System Design", "Risper", "A book about mastering system design", 5, 2014),
    Book(4, "Frontend A-Z", "Risper", "A comprehensive guide to frontend development", 5, 2016),
    Book(5, "Hello Architect", "Risper", "A book about software architecture principles", 5, 2018),

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



@app.get("/books/{book_id}")
def read_book_id(book_id: int = Path(gt=0)): #validating path parameters
    for book in BOOKS:
        if book.id == book_id:
            return book


@app.get("/books/")
def read_book_by_rating(rating:int):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return


@app.put("/books/update_book")
def update_book(book_request: BookRequest):
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_request.id:
            BOOKS[i] = book_request
            return BOOKS[i]
   
@app.delete("/books/delete_book/{book_id}")
def delete_book(book_id:int = Path(gt=0)): #validating path parameters
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            break

#assignment
@app.get("/books/search/{published_date}")
def read_book_by_publish_date(published_date: int):
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return        