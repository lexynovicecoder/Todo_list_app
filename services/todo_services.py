from fastapi import  Response, Depends, HTTPException, status
from Models.models import *
from sqlmodel import Session,select
from database.database import *
from typing import List






def get_session():
    with Session(engine) as session:
        yield session  # Yield the session for use in endpoints


def todo_service(response: Response, session: Session = Depends(get_session)):
    return TodoServices(session=session, response=response)




class TodoServices:
    def __init__(self,session,response):
        self.session = session  # Database session
        self.response = response
    
    def create_todo(self, task, user_payload):
        userid: int =  user_payload.get('id')
        db_item = Todo(**task.model_dump())
        todolist = self.session.get(TodoList, db_item.todolist_id)
        if todolist:
            if todolist.user_id != userid:
                raise HTTPException(status_code=404, detail="Task Not Found")
            db_item.user_id = userid
    
            self.session.add(db_item)
            self.session.commit()
            self.session.refresh(db_item)
            self.response.status_code = status.HTTP_201_CREATED
            return db_item
        else:
            raise HTTPException(status_code=404,detail="Todolist Not Created Yet")
        
    def read_todos(self,user_payload):
        userid: int =  user_payload.get('id')
        statement = select(Todo).where(Todo.user_id == userid)

        return self.session.exec(statement).all()
    
    def update_todo(self,id,task, user_payload):
        userid: int =  user_payload.get('id')
        task_item = self.session.get(Todo, id)
        if task_item:
            if task_item.user_id != userid:
                raise HTTPException(status_code=404, detail="Task Not Found!")
        
            if task_item.is_completed is True:
                raise HTTPException(status_code=404,detail="Task is Completed")
        else:
            raise HTTPException(status_code=404, detail="Task Not Found!")

        task_data = task.model_dump(exclude_unset=False)
        for key, value in task_data.items():
            setattr(task_item, key, value)
        self.session.add(task_item)
        self.session.commit()
        self.session.refresh(task_item)
        return task_item
    
    def complete_todo(self,id,user_payload):
        task_item = self.session.get(Todo, id)
        userid: int =  user_payload.get('id')

        if not task_item:
            raise HTTPException(status_code=404, detail="Task Not Found!")
        if task_item.user_id != userid:
            raise HTTPException(status_code=404, detail="Task Not Found!")
        if task_item.is_completed:
            raise HTTPException(status_code=401, detail="Already Completed")
        task_item.is_completed = True
        task_item.completed_at = datetime.now()
        todolist = self.session.get(TodoList, task_item.todolist_id)
        todolist.completed_tasks += 1
        self.session.add(task_item)
        self.session.commit()
        self.session.refresh(task_item)
        return task_item

    def undo_todo(self,id,user_payload):
        userid: int =  user_payload.get('id')
        task_item = self.session.get(Todo, id)
        if not task_item:
            raise HTTPException(status_code=404, detail="Task Not Found!")
        if task_item.user_id != userid:
            raise HTTPException(status_code=404, detail="Task Not Found!")       
        if not task_item.is_completed:
            raise HTTPException(status_code=401, detail="Cannot Undo")
        task_item.is_completed = False  
        task_item.completed_at = None
        todolist = self.session.get(TodoList, task_item.todolist_id)
        todolist.completed_tasks -= 1
        self.session.add(task_item)
        self.session.commit()
        self.session.refresh(task_item)
        return task_item
    
    def delete_todo(self,id,user_payload):
        userid: int =  user_payload.get('id')
        task = self.session.get(Todo, id)
        if not task :
            raise HTTPException(status_code=404, detail="Task hasn't been created")
        if task.user_id != userid:
            raise HTTPException(status_code=404, detail="Task hasn't been created")

        self.session.delete(task)
        self.session.commit()
        self.response.status_code = status.HTTP_204_NO_CONTENT
        return self.response.status_code




