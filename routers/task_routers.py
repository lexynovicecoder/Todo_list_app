from fastapi import  Response, status, Depends, HTTPException
from fastapi import APIRouter
from Models.models import *
from DTOs.dtos import TaskCreateDTO
from sqlmodel import Session, create_engine, SQLModel, select
from sqlalchemy import event
from sqlalchemy.orm.attributes import get_history
from datetime import datetime
from database.database import *
from typing import List



router1 = APIRouter(tags=["Todos"])


connect_args = {"check_same_thread": False}  # enables multi-thread access
engine = create_engine(DATABASE_URL, echo=True, connect_args=connect_args)



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

@event.listens_for(Todo,"after_update")
def after_task_completed(mapper, connection, target):
    if target.is_completed is True:
        with Session(bind=connection) as session:
            todolist = session.get(TodoList, target.todolist_id)  
            if todolist:
                todolist.completed_tasks += 1
                if todolist.completed_tasks == todolist.task_number:
                    todolist.is_completed = True
                session.commit() 

@event.listens_for(Todo,"before_update")
def after_task_undone(mapper, connection, target):
    history = get_history(target, "is_completed")
    if history.has_changes:
        if history.deleted:
            if history.deleted[-1] == True:
                if target.is_completed is False:
                    with Session(bind=connection) as session:
                        todolist = session.get(TodoList, target.todolist_id)
                        todolist.is_completed = False
                        if todolist:
                            todolist.completed_tasks -= 1
                            session.commit() 




@event.listens_for(Todo,"before_delete")
def deleted_todo(mapper,connection,target):
   with Session(bind=connection) as session:
        todolist = session.get(TodoList, target.todolist_id)  
        todolist.task_number -= 1
        if todolist.is_completed == True:
            todolist.completed_tasks -= 1
        session.commit()



def get_session():
    with Session(engine) as session:
        yield session  # Yield the session for use in endpoints




@router1.post("",response_model=Todo, status_code = 201 )
def create_task(task: TaskCreateDTO,response: Response, session: Session = Depends(get_session)):
    db_item = Todo(**task.model_dump())  # created_at and updated_at will be set automatically by the event
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    response.status_code = status.HTTP_201_CREATED
    return db_item

@router1.get("", response_model=List[Todo])
def read_tasks(session: Session = Depends(get_session)):
    tasks = session.exec(select(Todo)).all()  # Query the database for all Task records
    return tasks



@router1.get("/{task_id}/", response_model=Todo)
def read_task(task_id: int, session: Session = Depends(get_session)):
    task = session.get(Todo, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task Not Found!")
    return task

@router1.put("/{task_id}", response_model=Todo)
def update_task(task_id: int, task: TaskCreateDTO, session: Session = Depends(get_session)):
    task_item = session.get(Todo, task_id)
    if not task_item:
        raise HTTPException(status_code=404, detail="Task Not Found!")
    if task_item.is_completed is True:
        raise HTTPException(status_code=404,detail="Task is Completed")
    task_data = task.model_dump(exclude_unset=False)
    for key, value in task_data.items():
        setattr(task_item, key, value)
    session.add(task_item)
    session.commit()
    session.refresh(task_item)
    return task_item

@router1.patch("/{task_id}/complete", response_model=Todo)
def complete_task(task_id: int, session: Session = Depends(get_session)):
    task_item = session.get(Todo, task_id)
    if not task_item:
        raise HTTPException(status_code=404, detail="Task Not Found!")
    if task_item.is_completed:
        raise HTTPException(status_code=401, detail="Already Completed")
    task_item.is_completed = True

    session.add(task_item)
    session.commit()
    session.refresh(task_item)
    return task_item

@router1.patch("/{task_id}/undo", response_model=Todo)
def undo_task(task_id: int, session: Session = Depends(get_session)):
    task_item = session.get(Todo, task_id)
    if not task_item:
        raise HTTPException(status_code=404, detail="Task Not Found!")
    if not task_item.is_completed:
        raise HTTPException(status_code=401, detail="Cannot Undo")
    task_item.is_completed = False

    session.add(task_item)
    session.commit()
    session.refresh(task_item)
    return task_item


@router1.delete("/{task_id}", status_code = 204)
def delete_task(task_id: int, response: Response,session: Session = Depends(get_session)):
    task = session.get(Todo, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task hasn't been created")
    session.delete(task)
    session.commit()
    response.status_code = status.HTTP_204_NO_CONTENT
    return response.status_code

