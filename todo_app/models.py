from datetime import datetime
from sqlmodel import Field, SQLModel


class TodoBase(SQLModel):
    title: str
    completed: bool

class Todo(TodoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(default=datetime.now())
    updated_at: datetime | None = Field(default=datetime.now())

class TodoCreate(TodoBase):
    pass

class TodoRead(TodoBase):
    id: int
    created_at: datetime
    updated_at: datetime

class TodoUpdate(SQLModel):
    title: str | None
    completed: bool | None
    updated_at: datetime = Field(default=datetime.now())