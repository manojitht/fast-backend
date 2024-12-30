from fastapi import FastAPI, Response
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    ratings: Optional[int] = None

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hey there!!!!!"}

@app.post("/posts")
def create_posts(post: Post):
    print(post.dict())
    return {"content": post}
