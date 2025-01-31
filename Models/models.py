from typing import Optional,List
from sqlmodel import Field, SQLModel,Relationship
from datetime import datetime,timedelta



class TodoList(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.now)  # Default factory for current timestamp
    updated_at: Optional[datetime] = Field(default_factory=None)
    completed_tasks: Optional[int] = Field(default=0)  # Default value
    task_number: Optional[int] = Field(default=0)  # Default value
    tasks: List["Todo"] = Relationship(back_populates="todolist",sa_relationship_kwargs={"cascade": "all, delete-orphan"})

class Todo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    is_completed: bool = Field(default=False)  # Default value for is_completed
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)  # Default factory for current timestamp
    completed_at: Optional[datetime] = Field(default_factory=None)
    deadline: Optional[datetime] = Field(default=datetime.now()+timedelta(days=1))
    updated_at: Optional[datetime] = Field(default_factory=None)
    todolist_id: int = Field(default=None,foreign_key="todolist.id")
    todolist: Optional[TodoList] = Relationship(back_populates="tasks")


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    username: str = Field(index=True)
    first_name: str
    last_name: str
    email: str
    disabled: Optional[bool]=Field(default=False)
    hashed_password: str
    

