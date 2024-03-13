from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session, select
from todo_app.settings import DATABASE_URL
from todo_app.models import Todo, TodoCreate, TodoUpdate


connection_string = str(DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

# recycle connections after 5 minutes
# to correspond with the compute scale down
engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# The first part of the function, before the yield, will
# be executed before the application starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    print("Tables created..")
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/todos/")
def create_todo(todo: TodoCreate):
    with Session(engine) as session:
        db_todo = Todo.model_validate(todo)
        print(db_todo)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo
    

@app.get("/todos/")
def read_todos():
    with Session(engine) as session:
        todos = session.exec(select(Todo)).all()
        return todos
    
@app.get("/todos/{todo_id}")
def read_todo(todo_id: int):
    with Session(engine) as session:
        todo = session.get(Todo, todo_id)
        return todo
    
@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoUpdate):
    with Session(engine) as session:
        db_todo = session.get(Todo, todo_id)
        if not db_todo:
            return {"error": "Todo not found"}
        todo_data = todo.model_dump(exclude_unset=True)
        for key, value in todo_data.items():
            setattr(db_todo, key, value)
        session.add(db_todo)
        session.commit()
        session.refresh(db_todo)
        return db_todo
    
@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    with Session(engine) as session:
        db_todo = session.get(Todo, todo_id)
        if not db_todo:
            return {"error": "Todo not found"}
        session.delete(db_todo)
        session.commit()
        return {"message": "Todo deleted successfully"}