from pydantic import BaseModel, Field
from typing import Optional
from sqlmodel import Field, SQLModel, Session, create_engine, select


# Model: Pydantic Model + SQL Model

class BookBase(SQLModel):
    title: str = Field(index=True)  # setting index to true creates an index on the title column
    # making it easier to query for book titles
    author: str
    isbn: str = Field(min_length=4, max_length=5, default_factory=lambda: "0011")  # within the field are min_length
    # and max_length that ensures isbn conforms to a specific format default_factory ensures new instances of
    # BookModel have a predefined value if none is explicitly set
    description: Optional[str]  # making this attribute optional. No error is raised when not set


class Book(BookBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
