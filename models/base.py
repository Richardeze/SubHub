from sqlalchemy import create_engine
DATABASE_URL = "sqlite:///subhub.db"
engine = create_engine(DATABASE_URL, echo=True)

from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass