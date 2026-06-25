from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.core.config import settings


# Create the SQLAlchemy engine used to communicate with the database.
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  
)


# Factory for creating database sessions.
SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine,
)


# Base class that all SQLAlchemy models inherit from.
Base = declarative_base()


def get_db():
    """
    Provide a database session for each request.

    The session is automatically closed after the request completes,
    regardless of whether it succeeds or fails.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()