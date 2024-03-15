from sqlmodel import select
from fastapi import APIRouter, HTTPException
from todo_app.api.deps import SessionDep, CurrentUser
from todo_app.core.security import get_password_hash
from todo_app.models import User, UserCreate, UserUpdate

router = APIRouter()

@router.post("/super_users/", response_model=User)
def create_super_user(session: SessionDep, user_create: UserCreate):
    db_user = User.model_validate(user_create,update={"hashed_password": get_password_hash(user_create.hashed_password)})
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/users/", response_model=User)
def create_user(session: SessionDep,currentUser: CurrentUser ,user_create: UserCreate):
    db_user = User.model_validate(user_create,update={"hashed_password": get_password_hash(user_create.hashed_password)})
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
    
@router.get("/users/",response_model=list[User])
def read_users(session: SessionDep,currentUser: CurrentUser,skip: int = 0, limit: int = 10):
    users = session.exec(select(User).offset(skip).limit(limit)).all()
    return users
    
@router.get("/users/{user_id}", response_model=User)
def read_user(session: SessionDep,currentUser:CurrentUser,user_id: int):
    user = session.get(User, user_id)
    return user
    
@router.put("/users/{user_id}", response_model=User)
def update_user(session: SessionDep,currentUser:CurrentUser,user_id: int, user: UserUpdate):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.id != currentUser.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    user_data = user.model_dump(exclude_unset=True)
    extra_data = {}
    if "hashed_password" in user_data:
        password = user_data["hashed_password"]
        hashed_password = get_password_hash(password)
        extra_data["hashed_password"] = hashed_password
    db_user.sqlmodel_update(user_data, update=extra_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

    
@router.delete("/users/{user_id}", response_model=dict)
def delete_user(session: SessionDep,currentUser:CurrentUser,user_id: int):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    if db_user.id != currentUser.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    session.delete(db_user)
    session.commit()
    return {"message": "User deleted successfully"}