from fastapi import FastAPI
import argparse
import uvicorn
from routers.task_routers import engine
from database.database import *
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from routers.task_routers import router1
from routers.todoList_routers import router2
from routers.user_routers import router_user

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

app.include_router(router_user,tags=['Auth'])
app.include_router(router2,prefix="/todo-lists")
app.include_router(router1,prefix="/tasks")







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
