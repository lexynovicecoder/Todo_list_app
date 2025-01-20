from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime,timedelta



class Todo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    is_completed: bool = Field(default=False)  # Default value for is_completed
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)  # Default factory for current timestamp
    deadline: Optional[datetime] = Field(default=datetime.now()+timedelta(days=1))

    updated_at: Optional[datetime] = Field(default_factory=None)





