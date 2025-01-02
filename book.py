from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()

class Books(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=101)

book_db = []

@app.get("/")
def root():
    return book_db

@app.post("/")
def add_book(Book: Books):
    book_db.append(Book)
    return {"message": f"yo've added {Book.title} to book store."}

@app.put("/{book_id}")
def update_book(book_id: UUID, book: Books):
    count = 0
    for x in book_db:
        count += 1
        if x.id == book_id:
            book_db[count - 1] = book
            return book_db[count - 1]
    raise HTTPException(
        status_code=404,
        detail=f"There is no book found with {book_id}."
    )

@app.delete("/{book_id}")
def delete_book(book_id: UUID):
    count = 0
    for x in book_db:
        count += 1
        if x.id == book_id:
            del book_db[count - 1]
            return f"The book is {book_id} was deleted!"
    raise HTTPException(
        status_code=404,
        detail=f"There is no book found with {book_id}."
    )