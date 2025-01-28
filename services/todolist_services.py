from fastapi import status,HTTPException
from Models.models import *
from DTOs.dtos import TodoListCreateDTO
from sqlmodel import Session,select
from database.database import *
from typing import List
from routers.task_routers import engine

def get_session():
    with Session(engine) as session:
        yield session  # Yield the session for use in endpoints


class TodolistServices:
    def __init__(self,session,response):
        self.session = session  # Database session
        self.response = response
    
    def create_todolist(self, task: TodoListCreateDTO):
        db_item = TodoList(**task.model_dump())
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        self.response.status_code = status.HTTP_201_CREATED
        return db_item
    
    def read_todolists(self):
        return self.session.exec(select(TodoList)).all() 
    
    def read_todolist(self, id):
        todolist = self.session.get(TodoList, id)
        if not todolist:
            raise HTTPException(status_code=404, detail="TodoList not found")
        return todolist
    
    def update_todolist(self, id,task):
        todolist_item = self.session.get(TodoList, id)
        if not todolist_item:
            raise HTTPException(status_code=404, detail="Task Not Found!")
        todolist_data = task.model_dump(exclude_unset=False)
        for key, value in todolist_data.items():
            setattr(todolist_item, key, value)
        self.session.add(todolist_item)
        self.session.commit()
        self.session.refresh(todolist_item)
        return todolist_item
    
    def delete_todolist(self, id):
        todolist = self.session.get(TodoList, id)
        if not todolist:
            raise HTTPException(status_code=404, detail="Task hasn't been created")
        self.session.delete(todolist)
        self.session.commit()
        self.response.status_code = status.HTTP_204_NO_CONTENT
        return self.response.status_code


