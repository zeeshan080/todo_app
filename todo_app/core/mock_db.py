from collections.abc import Generator
from sqlalchemy import create_engine
from sqlmodel import Session
from sqlmodel import SQLModel
from todo_app.settings import DATABASE_URL_TEST


connection_string = str(DATABASE_URL_TEST).replace(
    "postgresql", "postgresql+psycopg"
)
test_engine = create_engine(
    connection_string, connect_args={"sslmode": "require"}, pool_recycle=300
)

def get_test_db() -> Generator[Session, None, None]:
    # print("--> TEST DB HERE <---")
    with Session(test_engine) as session:
        yield session


def create_db_and_tables():
    print("Creating tables for testing..")
    SQLModel.metadata.create_all(test_engine)
    return ("Tables created..")

def drop_tables():
    print("Dropping tables..")
    SQLModel.metadata.drop_all(test_engine)
    return ("Tables dropped..")