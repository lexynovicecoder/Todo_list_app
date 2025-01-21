from fastapi import FastAPI
import argparse
import uvicorn
from task_router import engine
from database.database import *
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from task_router import router

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



app.include_router(router,prefix="/tasks")







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
