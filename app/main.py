from fastapi import FastAPI, HTTPException, Depends
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


@app.get("/sqlalchemy")
def tests_posts(db: Session=Depends(get_db)):
    posts = db.query(models.Posts).all()
    return {"status", posts}


# if __name__ == "__main__":
#     uvicorn.run("app.main:app", host="127.0.0.1", port=8080, reload=True)