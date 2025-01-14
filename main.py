from fastapi import FastAPI
import argparse
import uvicorn
from sqlmodel import Session
from models import *

app = FastAPI()


@app.get('/')
def example():
    return {"title": "Example"}

@app.post("/books")
def create_book(book: BookModel):
    with Session() as session:  # a session is used to manage database interactions(adding,querying,updating etc)
        db_item = book
        session.add(db_item)  # adds BookModel instance to session but it is pending
        session.commit()  # writes all pending changes to database
        session.refresh(db_item)  # refresh instance
        return db_item


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
