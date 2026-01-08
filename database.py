from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# DATABASE CONNECTION STRING
DATABASE_URL = "sqlite:///subhub.db"

# Create the database engine
engine = create_engine(
    DATABASE_URL,
    echo=True  # shows SQL queries in the terminal (good for learning)
)

# Session factory (used later, not now)
SessionLocal = sessionmaker(bind=engine,
                            autoflush=False,
                            autocommit=False)
