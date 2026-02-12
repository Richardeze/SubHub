from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base

# DATABASE CONNECTION STRING
DATABASE_URL = "sqlite:///subhub.db"

# Create the database engine
engine = create_engine(
    DATABASE_URL,
    echo=True,  # shows SQL queries in the terminal
    connect_args={"check_same_thread": False}  # Required for SQLite with FastAPI
)

# Session factory (used later, not now)
SessionLocal = sessionmaker(bind=engine,
                            autoflush=False,
                            autocommit=False)


# Dependency function for FastAPI
def get_db():
    """
    Provides a database session to route handlers.
    Automatically closes the session when done.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()