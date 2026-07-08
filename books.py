from fastapi import FastAPI

app = FastAPI()





@app.get("/books")
def first_api():
    return {"message": "building my first API!"}