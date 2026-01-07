import logging
from sqlmodel import SQLModel, create_engine, Session

logger = logging.getLogger("paintingexhibition.db")

DATABASE_URL = "sqlite:///./painting_exhibition.db"
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    """Dependency that yields a DB session (generator function). Do NOT decorate with @contextmanager.

    FastAPI will use this generator as a dependency context manager.
    """
    logger.debug("Opening DB session")
    with Session(engine) as session:
        try:
            yield session
        finally:
            logger.debug("Closing DB session")