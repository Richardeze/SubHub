from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class GroupMember(Base):
    __tablename__ = "group_members"
    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    payment_status = Column(String, default="pending")  # pending, paid
    joined_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    group = relationship("Group", back_populates="members")
    user = relationship("User", back_populates="memberships")