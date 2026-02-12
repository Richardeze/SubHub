from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False) # Netflix, Spotify, Apple music etc
    total_slots = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)

    groups = relationship("Group", back_populates="subscription")
    group_requests = relationship("GroupRequest", back_populates="subscription")

# ADD: Property to calculate base_price_per_slot when needed
    @property
    def base_price_per_slot(self):
        """Calculate base price per slot automatically"""
        return self.total_price // self.total_slots  # Integer division