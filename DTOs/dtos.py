from pydantic import BaseModel
from datetime import datetime,timedelta
from typing import Optional
from sqlmodel import Field



class TaskCreateDTO(BaseModel):
    todolist_id: int 
    name: str 
    is_completed: bool = Field(default=False)  # Default value for is_completed   
    deadline: Optional[datetime] = Field(default=datetime.now()+timedelta(days=1))
    description: Optional[str] = None

class TodoListCreateDTO(BaseModel):
    name: str = Field(index=True)
    is_completed: bool = Field(default=False)  # Default value for is_completed
