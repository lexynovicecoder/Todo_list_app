from typing import Optional
from sqlmodel import Field, SQLModel, Session, create_engine, select
from datetime import datetime



class TodoList(SQLModel):
    name: str = Field(index=True)
    is_completed: bool = Field(default=False)  # Default value for is_completed
    deadline: Optional[datetime] = Field(default=None)
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)  # Default factory for current timestamp
    updated_at: Optional[datetime] = Field(default=None)


class Task(TodoList, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class TaskCreate(SQLModel):
    name: str
    is_completed: Optional[bool] = Field(default=False)
    deadline: Optional[datetime] = None
    description: Optional[str] = None


class TaskRead(TodoList):
    id: int
    updated_at: Optional[datetime] = None  # Explicitly set updated_at default to None


