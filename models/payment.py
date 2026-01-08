from sqlalchemy import Column, Integer, ForeignKey, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    plan_id = Column(Integer, ForeignKey("subscription_plans.id"))

    amount_paid = Column(Integer, nullable=False)

    # Join_payment | Owner_payout | Refund
    payment_type = Column(String, nullable=False)

    # Pending | Completed | Failed
    status = Column(String, default="PENDING")
    created_at =Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="payments")