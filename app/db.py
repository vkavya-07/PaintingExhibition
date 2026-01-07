from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "sqlite:///./painting_exhibition.db"
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

from contextlib import contextmanager

@contextmanager
def get_session():
    with Session(engine) as session:
        yield session