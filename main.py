from fastapi import FastAPI, Response, status, Depends, HTTPException
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


@app.get("/tasks", response_model=List[TodoList])
def read_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(TodoList)).all()  # Query the database for all Task records
    return tasks


@app.post("/tasks", response_model=TodoList, status_code = 201 )
def create_task(task: TaskCreateDTO,response: Response, session: Session = Depends(get_session)):
    db_item = TodoList(**task.model_dump())  # created_at and updated_at will be set automatically by the event
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    response.status_code = status.HTTP_201_CREATED
    return db_item


@app.get("/tasks/{task_id}", response_model=TodoList)
def read_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(TodoList, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task Not Found!")
    return task

@app.put("/tasks/{task_id}", response_model=TodoList)
def update_task(task_id: int, task: TaskCreateDTO, session: Session = Depends(get_session)):
    task_item = session.get(TodoList, task_id)
    if not task_item:
        raise HTTPException(status_code=404, detail="Task Not Found!")
    task_data = task.model_dump(exclude_unset=False)
    for key, value in task_data.items():
        setattr(task_item, key, value)
    task_item.updated_at = datetime.now()

    session.add(task_item)
    session.commit()
    session.refresh(task_item)
    return task_item

@app.patch("/tasks/{task_id}/complete", response_model=TodoList)
def complete_task(task_id: int, session: Session = Depends(get_session)):
    task_item = session.get(TodoList, task_id)
    if not task_item:
        raise HTTPException(status_code=404, detail="Task Not Found!")
    if task_item.is_completed:
        raise HTTPException(status_code=401, detail="Already Completed")
    task_item.updated_at = datetime.now()
    task_item.is_completed = True

    session.add(task_item)
    session.commit()
    session.refresh(task_item)
    return task_item

@app.patch("/tasks/{task_id}/undo", response_model=TodoList)
def undo_task(task_id: int, session: Session = Depends(get_session)):
    task_item = session.get(TodoList, task_id)
    if not task_item:
        raise HTTPException(status_code=404, detail="Task Not Found!")
    if not task_item.is_completed:
        raise HTTPException(status_code=401, detail="Cannot Undo")
    task_item.updated_at = datetime.now()
    task_item.is_completed = False

    session.add(task_item)
    session.commit()
    session.refresh(task_item)
    return task_item


@app.delete("/tasks/{task_id}", status_code = 204)
def delete_task(task_id: int, response: Response,session: Session = Depends(get_session)):
    task = session.get(TodoList, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task hasn't been created")
    session.delete(task)
    session.commit()
    response.status_code = status.HTTP_204_NO_CONTENT
    return response.status

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
