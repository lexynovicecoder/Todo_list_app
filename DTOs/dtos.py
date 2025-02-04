from pydantic import BaseModel
from datetime import datetime,timedelta
from typing import Optional,List
from sqlmodel import Field
from Models.models import Todo,User



class TaskCreateDTO(BaseModel):
    name: str 
    deadline: Optional[datetime] = Field(default=datetime.now()+timedelta(days=1))
    description: Optional[str] = None
    todolist_id: int

class TaskUpdateDTO(BaseModel):
    name: str 
    deadline: Optional[datetime] = Field(default=datetime.now()+timedelta(days=1))
    description: Optional[str] = None

class TodoListCreateDTO(BaseModel):
    name: str = Field(index=True)
    user_id: int

class TodoListUpdateDTO(BaseModel):
    name: str = Field(index=True)

class LoginDTO(BaseModel):
    username: str = Field(index=True)
    password: str



class TodoListResponseDTO(BaseModel):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.now)  # Default factory for current timestamp
    updated_at: Optional[datetime] = Field(default_factory=None)
    completed_tasks: Optional[int] = Field(default=0)  # Default value
    task_number: Optional[int] = Field(default=0)  # Default value
    tasks: List[Todo] = []

class CreateUserDTO(BaseModel):
    email: str
    first_name: str
    last_name: str
    username: str
    password: str



