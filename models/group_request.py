from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class GroupRequest(Base):
    __tablename__ = "group_requests"

    id = Column(Integer, index=True, primary_key=True)
    requester_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    subscription_id = Column(Integer, ForeignKey("subscriptions.id"), nullable=False)

    sub_start_date = Column(DateTime, nullable=False)
    sub_end_date = Column(DateTime, nullable=False)
    renewal_date = Column(DateTime, nullable=False)
    total_slots = Column(Integer, nullable=False)
    payment_method = Column(String, nullable=False) # "card", "wallet", "bank_transfer"

    card_expiry = Column(String, nullable=True)  # MM/YY — ONLY if payment_method == "card"
    proof_url = Column(String, nullable=True)

    status = Column(String, default="pending")  # Pending, Approved, Rejected
    rejection_reason = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    # Relationships
    requester = relationship("User", back_populates="group_requests")
    subscription = relationship("Subscription", back_populates="group_requests")