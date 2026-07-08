from fastapi import Body, FastAPI

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
    