from fastapi import FastAPI, Depends, HTTPException
import argparse
import uvicorn
from sqlmodel import Session, create_engine
from database import *
from models import *
from typing import List
from contextlib import asynccontextmanager


connect_args = {"check_same_thread": False}  # enables multi-thread access
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)


def get_session():
    with Session(engine) as session:
        yield session  # Yield the session for use in endpoints


def create_db_and_table():
    SQLModel.metadata.create_all(engine)  # creates table for model


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_table()
    yield

app = FastAPI(lifespan=lifespan)


@app.get('/')
def example():
    return {"Title": "Todo list"}


# @app.get("/books", response_model=List[Book])
# def read_books():
#     with Session(engine) as session:
#         books = session.exec(select(Book)).all()
#         return books
#
#
@app.post("/Tasks", response_model=TaskRead)
def create_task(task: TaskCreate, session: Session = Depends(get_session)):
    db_item = Task.model_validate(task)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item


# @app.get("/books/{book_id}",response_model=Book)
# def read_book(book_id: int):
#     with Session(engine) as session:
#         book_item = session.get(Book,book_id)
#         if not book_item:
#             raise HTTPException(status_code=404, detail="Book Not Found!")
#         return book_item
#
# @app.patch("/books/{book_id}", response_model=Book)
# def update_book(book_id: int, book: Book):
#     with Session(engine) as session:
#         book_item = session.get(Book, book_id)
#         if not book_item:
#             raise HTTPException(status_code=404, detail="Book Not Found!")
#         book_data = book.dict(exclude_unset=True)
#         for key, value in book_data.items():
#             setattr(book_item, key, value)
#         session.add(book_item)
#         session.commit()
#         session.refresh(book_item)
#         return book_item
#
# @app.delete("/books/{book_id}")
# def delete_book(book_id: int):
#     with Session(engine) as session:
#         book_item = session.get(Book, book_id)
#         if not book_item:
#             raise HTTPException(status_code=404, detail="Book Not Found!")
#         session.delete(book_item)
#         session.commit()
#         return {"ok": True}
#
#
#
#

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run FastAPI with optional file watching.")
    parser.add_argument("--watch", action="store_true", help="Enable auto-reload for the server.")
    args = parser.parse_args()

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000,
        reload=args.watch  # Enable reload if --watch flag is passed
    )
