from fastapi import APIRouter
from todo_app.api.routes import todos, users, login

api_router = APIRouter()

api_router.include_router(login.router, tags=["Login"])
api_router.include_router(todos.router, tags=["Todos"])
api_router.include_router(users.router, tags=["Users"])

