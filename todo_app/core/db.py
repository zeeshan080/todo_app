from sqlalchemy import create_engine
from sqlmodel import SQLModel, Session
from todo_app.settings import DATABASE_URL
from collections.abc import Generator

connection_string = str(DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg"
)

# recycle connections after 5 minutes
# to correspond with the compute scale down
engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)

def get_db() -> Generator[Session, None, None]:
    print("--> REAL DB HERE <---")
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
