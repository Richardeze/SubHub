from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"))
    host_user_id = Column(Integer, ForeignKey("users.id"))

    slots_filled = Column(Integer, default=1)
    status = Column(String, default="open")  # open, full, active
    renewal_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    subscription = relationship("Subscription", back_populates="groups")
    host = relationship("User", back_populates="groups_hosted")
    members = relationship("GroupMember", back_populates="group")