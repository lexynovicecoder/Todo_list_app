from fastapi import  Response, Depends, HTTPException, status
from Models.models import *
from DTOs.dtos import TodoListCreateDTO
from sqlmodel import Session,select
from database.database import *
from typing import List
from database.database import engine


def get_session():
    with Session(engine) as session:
        yield session  # Yield the session for use in endpoints


def todolist_service(response: Response, session: Session = Depends(get_session)):
    return TodolistServices(session=session, response=response)
    
class TodolistServices:
    def __init__(self,session,response):
        self.session = session  # Database session
        self.response = response
    
    def create_todolist(self, task: TodoListCreateDTO, user_payload):
        userid: int =  user_payload.get('id')
        db_item = TodoList(**task.model_dump())
        user =  self.session.get(User, db_item.user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not Found")
        if user.id != userid:
            raise HTTPException(status_code=401, detail="Unauthorized")
        self.session.add(db_item)
        self.session.commit()
        self.session.refresh(db_item)
        self.response.status_code = status.HTTP_201_CREATED
        return db_item
    
    def read_todolists(self,user_payload):
        userid: int =  user_payload.get('id')
        statement = select(TodoList).where(TodoList.user_id == userid)
        user = self.session.exec(statement).all()
        return user 
    
    def read_todolist(self, id, user_payload):
        userid: int =  user_payload.get('id')
        todolist = self.session.get(TodoList, id)
        if todolist.user_id != userid:
            raise HTTPException(status_code=404, detail="TodoList not found")
        return todolist
    
    def update_todolist(self, id,task,user_payload):
        userid: int =  user_payload.get('id')
        todolist_item = self.session.get(TodoList, id)
        if not todolist_item:
            raise HTTPException(status_code=404, detail="Todolist Not Found!")
        if todolist_item.user_id != userid:
            raise HTTPException(status_code=401, detail="Unauthorized")
        todolist_data = task.model_dump(exclude_unset=False)  
        for key, value in todolist_data.items(): 
            setattr(todolist_item, key, value)
        self.session.add(todolist_item)
        self.session.commit()
        self.session.refresh(todolist_item)
        return todolist_item
    
    def delete_todolist(self, id, user_payload):
        userid: int =  user_payload.get('id')
        todolist = self.session.get(TodoList, id)
        if not todolist:
            raise HTTPException(status_code=404, detail="Task hasn't been created")
        if todolist.user_id != userid:
            raise HTTPException(status_code=401, detail="Unauthorized")
        self.session.delete(todolist)
        self.session.commit()
        self.response.status_code = status.HTTP_204_NO_CONTENT
        return self.response.status_code


