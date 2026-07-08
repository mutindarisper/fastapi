from fastapi import Body, FastAPI
from pydantic import BaseModel

app = FastAPI()

BOOKS = [
    {"title": "Title One", "author": "Author One", "category": "science"},
    {"title": "Title Two", "author": "Author Two", "category": "math"},
    {"title": "Title Three", "author": "Author Three", "category": "history"},
    {"title": "Title Four", "author": "Author Four", "category": "science"},
    {"title": "Title Five", "author": "Author Five", "category": "math"}
]

@app.get("/books")
def read_all_books():
    return BOOKS

#path parameters
    
@app.get("/books/{book_title}")
def read_book(book_title: str):
    for book in BOOKS:
        if book["title"].casefold() == book_title.casefold():
            return book
        

  
#query parameters

@app.get("/books/")
def read_category_by_query(category:str):
    books_to_return = []
    for book in BOOKS:
        if book["category"].casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


#path and query parameters combined
@app.get("/books/{book_author}/")
def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book["author"].casefold() == book_author.casefold() and book["category"].casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return





#post request

@app.post("/books/create_book")
def create_book(new_book=Body()):
    BOOKS.append(new_book)
    return BOOKS

#PUT method

@app.put("/books/update_book")
def update_books(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i]["title"].casefold() == updated_book["title"].casefold():
            BOOKS[i] = updated_book



    
#delete method

@app.delete("/books/delete_book/{book_title}")
def delete_book(book_title: str):
    for book in BOOKS:
        if book["title"].casefold() == book_title.casefold():
            BOOKS.remove(book)


#assignment
@app.get("/books/author/{book_author}")
def read_author(book_author:str):
    books_to_return = []
    for book in BOOKS:
        if book["author"].casefold() == book_author.casefold():
            books_to_return.append(book)
    return books_to_return


# new HTTP method: QUERY

BOOKS2 = [
    {
        "title": "Title One",
        "author": "Author One",
        "category": "science",
        "year": 2021,
        "publisher": "Pearson",
        "language": "English",
        "pages": 420,
        "rating": 4.8,
        "price": 2500,
        "available": True,
        "tags": ["physics", "space", "astronomy"]
    },
    {
        "title": "Title Two",
        "author": "Author Two",
        "category": "math",
        "year": 2019,
        "publisher": "O'Reilly",
        "language": "English",
        "pages": 310,
        "rating": 4.5,
        "price": 1800,
        "available": False,
        "tags": ["algebra", "calculus"]
    },
    
    
]


class BookSearchQuery(BaseModel):
    author: str | None = None
    category: str | None = None
    year: int | None = None
    publisher: str | None = None
    tags: list[str] | None = None


@app.api_route("/books/search", methods=["QUERY"])
def search_books(query: BookSearchQuery = Body(...)):
    books_to_return = []
    for book in BOOKS2:
        if (query.author is None or book["author"].casefold() == query.author.casefold()) and \
           (query.category is None or book["category"].casefold() == query.category.casefold()) and \
           (query.year is None or book["year"] == query.year) and \
           (query.publisher is None or book["publisher"].casefold() == query.publisher.casefold()) :
            books_to_return.append(book)
    return books_to_return