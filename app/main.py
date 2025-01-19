from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, Field
from .database import engine, Session, get_db
from . import models
import uvicorn

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class PostUpdate(BaseModel):
    title: str
    content: str


@app.get("/posts")
def get_posts(db: Session=Depends(get_db)):
    posts = db.query(models.Posts).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post, db: Session=Depends(get_db)):
    # new_post = models.Posts(title=post.title, content=post.content, published=post.published)
    new_post = models.Posts(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/post/{id}")
def get_post(id: int, db: Session=Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id}, was not found!")
    return post


@app.put("/post/{id}")
def update_post(id: int, updated_post: PostUpdate, db: Session=Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id}, was not found!")
    
    for key, value in updated_post.model_dump().items():
        setattr(post, key, value)
    
    db.commit()
    db.refresh(post)

    return f"The post id: {id} was updated!"
    

@app.delete("/post/{id}")
def delete_post(id: int, db: Session=Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id}, was not found!")
    db.delete(post)
    db.commit()
    return {"message", f"successfully deleted post id: {post.id}"}

# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host="127.0.0.1", port=8080, reload=True)