from fastapi import  Response, status, Depends, HTTPException
from fastapi import APIRouter
from models.models import TodoList
from DTOs.dtos import TodoListCreateDTO
from sqlmodel import Session
from sqlalchemy import event
from datetime import datetime
from database.database import *
from typing import List
from routers.task_routers import engine

router2 = APIRouter(tags=["TodoLists"])

def get_session():
    with Session(engine) as session:
        yield session  # Yield the session for use in endpoints

@router2.post("",response_model=TodoList, status_code = 201 )
def create_task(task: TodoListCreateDTO,response: Response, session: Session = Depends(get_session)):
    db_item = TodoList(**task.model_dump())  # created_at and updated_at will be set automatically by the event
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    response.status_code = status.HTTP_201_CREATED
    return db_item
