from typing import Optional
from sqlmodel import Field, SQLModel, Session, create_engine, select
from datetime import datetime,timedelta
from pydantic import BaseModel



class TodoList(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    is_completed: bool = Field(default=False)  # Default value for is_completed
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)  # Default factory for current timestamp
    deadline: Optional[datetime] = Field(default=datetime.now()+timedelta(days=1))

    updated_at: Optional[datetime] = Field(default_factory=None)




class TaskCreateDTO(BaseModel):
    name: str 
    is_completed: bool = Field(default=False)  # Default value for is_completed   
    deadline: Optional[datetime] = Field(default=datetime.now()+timedelta(days=1))
    description: Optional[str] = None

