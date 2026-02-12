from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    groups_hosted = relationship("Group", back_populates="host")
    memberships = relationship("GroupMember", back_populates="user")
    payments = relationship("Payment", back_populates="payer")
    wallet = relationship("Wallet", back_populates="user", uselist=False)
    group_requests = relationship("GroupRequest", back_populates="requester")


