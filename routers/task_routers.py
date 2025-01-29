from fastapi import Depends
from fastapi import APIRouter
from Models.models import *
from DTOs.dtos import TaskCreateDTO,TaskUpdateDTO
from sqlmodel import Session
from sqlalchemy import event
from datetime import datetime
from database.database import *
from typing import List
from services.todo_services import todo_service,TodoServices
from database.database import engine



router1 = APIRouter(tags=["Todos"])






@event.listens_for(Todo, "before_update")
def update_updated_at(mapper, connection, target):
    target.updated_at = datetime.now()


@event.listens_for(Todo, 'after_insert')
def after_insert_todo(mapper, connection, target):
    with Session(bind=connection) as session:
        todolist = session.get(TodoList, target.todolist_id)  
        if todolist:
            todolist.task_number += 1
        session.commit() 



@event.listens_for(Todo,"before_delete")
def deleted_todo(mapper,connection,target):
   with Session(bind=connection) as session:
        todolist = session.get(TodoList, target.todolist_id) 
        todolist.task_number -= 1 
        if not target.is_completed:
            session.commit()
            return
        todolist.completed_tasks -= 1
        session.commit()



def get_session():
    with Session(engine) as session:
        yield session  # Yield the session for use in endpoints




@router1.post("",response_model=Todo, status_code = 201 )
def create_task(task: TaskCreateDTO,todo_service: TodoServices = Depends(todo_service)):
    db_item = todo_service.create_todo(task)
    return db_item


@router1.get("", response_model=List[Todo])
def read_tasks(todo_service: TodoServices = Depends(todo_service)):
    tasks = todo_service.read_todos()
    return tasks



@router1.put("/{task_id}", response_model=Todo)
def update_task(task_id: int, task: TaskUpdateDTO,todo_service: TodoServices = Depends(todo_service)):
    task_item = todo_service.update_todo(id=task_id,task=task)
    return task_item

@router1.patch("/{task_id}/complete", response_model=Todo)
def complete_task(task_id: int, todo_service: TodoServices = Depends(todo_service)):
    completed_task = todo_service.complete_todo(task_id)
    return completed_task
    

@router1.patch("/{task_id}/undo", response_model=Todo)
def undo_task(task_id: int,todo_service: TodoServices = Depends(todo_service)):
    undone_task = todo_service.undo_todo(task_id)
    return undone_task



@router1.delete("/{task_id}", status_code = 204)
def delete_task(task_id: int,todo_service: TodoServices = Depends(todo_service)):
    deleted_task = todo_service.delete_todo(task_id)
    return deleted_task
    
