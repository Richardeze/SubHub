from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base

class Subscription(Base):
    __tablename__ = "subscriptions"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False) # Netflix, Spotify, Apple music etc
    total_slots = Column(Integer, nullable=False)
    total_price = Column(Integer, nullable=False)
    base_price_per_slot = Column(Integer, nullable=False)