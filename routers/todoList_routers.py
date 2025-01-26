from fastapi import  Response, status, Depends, HTTPException
from fastapi import APIRouter
from Models.models import *
from DTOs.dtos import TodoListCreateDTO,TodoListResponseDTO
from sqlmodel import Session,select
from sqlalchemy.orm import selectinload
from datetime import datetime
from database.database import *
from typing import List
from routers.task_routers import engine
from sqlalchemy import event


router2 = APIRouter(tags=["TodoLists"])

def get_session():
    with Session(engine) as session:
        yield session  # Yield the session for use in endpoints

@event.listens_for(TodoList, "before_update")
def update_updated_at(mapper, connection, target):
    target.updated_at = datetime.now()


@router2.post("",response_model=TodoList, status_code = 201 )
def create_todolist(task: TodoListCreateDTO,response: Response, session: Session = Depends(get_session)):
    db_item = TodoList(**task.model_dump())  # created_at and updated_at will be set automatically by the event
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    response.status_code = status.HTTP_201_CREATED
    return db_item

@router2.get("", response_model=List[TodoList])
def read_todoLists(session: Session = Depends(get_session)):
    todolists = session.exec(select(TodoList)).all()  # Query the database for all Task records
    return todolists


@router2.get("/{todolist_id}", response_model=TodoListResponseDTO)
def read_todolist(todolist_id: int, session: Session = Depends(get_session)):
    todolist = session.get(TodoList, todolist_id)
    if not todolist:
        raise HTTPException(status_code=404, detail="TodoList not found")

    return todolist


@router2.put("/{todolist_id}", response_model=TodoList)
def update_todolist(todolist_id: int, task: TodoListCreateDTO, session: Session = Depends(get_session)):
    todolist_item = session.get(TodoList, todolist_id)
    if not todolist_item:
        raise HTTPException(status_code=404, detail="Task Not Found!")
    todolist_data = task.model_dump(exclude_unset=False)
    for key, value in todolist_data.items():
        setattr(todolist_item, key, value)
    session.add(todolist_item)
    session.commit()
    session.refresh(todolist_item)
    return todolist_item


@router2.delete("/{todolist_id}", status_code = 204)
def delete_todolist(todolist_id: int, response: Response,session: Session = Depends(get_session)):
    todolist = session.get(TodoList, todolist_id)
    if not todolist:
        raise HTTPException(status_code=404, detail="Task hasn't been created")
    session.delete(todolist)
    session.commit()
    response.status_code = status.HTTP_204_NO_CONTENT
    return response.status_code

