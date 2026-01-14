from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    payer_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=False)

    amount_paid = Column(Integer, nullable=False)
    status = Column(String, default="pending") # pending, completed, refunded
    payment_type = Column(String, nullable=False) # Join_payment | Owner_payout | Refund
    created_at =Column(DateTime, default=datetime.utcnow)
    # Relationships
    payer = relationship("User", back_populates="payments")
    group = relationship("Group")