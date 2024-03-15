from sqlmodel import select
from fastapi import APIRouter, HTTPException
from todo_app.api.deps import SessionDep, CurrentUser
from todo_app.models import Todo, TodoCreate, TodoUpdate

router = APIRouter()


@router.post("/todos/", response_model=Todo)
def create_todo(session: SessionDep,currentUser: CurrentUser, todo: TodoCreate):
    db_todo = Todo.model_validate(todo,update={"user_id":currentUser.id})
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo
    
@router.get("/todos/", response_model=list[Todo])
def read_todos(session: SessionDep,currentUser: CurrentUser,skip: int = 0, limit: int = 10):
    todos = session.exec(select(Todo).where(Todo.user_id == currentUser.id).offset(skip).limit(limit)).all()
    return todos
    
@router.get("/todos/{todo_id}", response_model=Todo)
def read_todo(session: SessionDep,currentUser: CurrentUser,todo_id: int):
    todo = session.get(Todo, todo_id)
    if todo.user_id != currentUser.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return todo
    
@router.put("/todos/{todo_id}",response_model=Todo)
def update_todo(session: SessionDep,currentUser: CurrentUser,todo_id: int, todo: TodoUpdate):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    if db_todo.user_id != currentUser.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    todo_data = todo.model_dump(exclude_unset=True)
    for key, value in todo_data.items():
        setattr(db_todo, key, value)
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo
    
@router.delete("/todos/{todo_id}",response_model=dict)
def delete_todo(session: SessionDep,currentUser: CurrentUser,todo_id: int):
    db_todo = session.get(Todo, todo_id)
    if not db_todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(db_todo)
    session.commit()
    return {"message": "Todo deleted successfully"}