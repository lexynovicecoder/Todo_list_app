from fastapi import  Response, Depends
from fastapi import APIRouter
from Models.models import *
from DTOs.dtos import TodoListCreateDTO,TodoListResponseDTO,TodoListUpdateDTO
from datetime import datetime
from database.database import *
from typing import List
from routers.task_routers import engine
from sqlalchemy import event
from services.todolist_services import TodolistServices  # Assuming the service is in a services folder
from sqlmodel import Session
from services.user_service import get_current_user
from authorization_authentication import auth



router2 = APIRouter(tags=["TodoLists"])

def get_session():
    with Session(engine) as session:
        yield session  # Yield the session for use in endpoints


def todolist_service(response: Response, session: Session = Depends(get_session)):
    return TodolistServices(session=session, response=response)
    

@event.listens_for(TodoList, "before_update")
def update_updated_at(mapper, connection, target):
    target.updated_at = datetime.now()


@router2.post("",response_model=TodoList, status_code = 201 )
def create_todolist(task: TodoListCreateDTO,todolist_service: TodolistServices = Depends(todolist_service), payload: dict = Depends(auth.jwt_decode_token)):
    db_item = todolist_service.create_todolist(task,payload)
    return db_item

@router2.get("/", response_model=List[TodoList])
def read_todoLists(todolist_service: TodolistServices = Depends(todolist_service), payload: dict = Depends(auth.jwt_decode_token)):
    todolists = todolist_service.read_todolists(payload)
    return todolists


@router2.get("/{todolist_id}", response_model=TodoListResponseDTO)
def read_todolist(todolist_id: int, todolist_service: TodolistServices = Depends(todolist_service),payload: dict = Depends(auth.jwt_decode_token)):
    todolist = todolist_service.read_todolist(todolist_id,payload)
    return todolist

    


@router2.put("/{todolist_id}", response_model=TodoList)
def update_todolist(todolist_id: int,task: TodoListUpdateDTO, todolist_service: TodolistServices = Depends(todolist_service), payload: dict = Depends(auth.jwt_decode_token)):
    update = todolist_service.update_todolist(todolist_id, task, payload)
    return update
    


@router2.delete("/{todolist_id}", status_code = 204)
def delete_todolist(todolist_id: int, todolist_service: TodolistServices = Depends(todolist_service), payload: dict = Depends(auth.jwt_decode_token)):
    delete = todolist_service.delete_todolist(todolist_id,payload)
    return delete
    