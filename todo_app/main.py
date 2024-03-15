from contextlib import asynccontextmanager
from fastapi import FastAPI
from todo_app.api.main import api_router
from todo_app.core.db import create_db_and_tables


# The first part of the function, before the yield, will
# be executed before the application starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating tables..")
    create_db_and_tables()
    print("Tables created..")
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(api_router, prefix="/api/v1")