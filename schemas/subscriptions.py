from pydantic import BaseModel, Field
from  typing import   List, Optional
from datetime import datetime

# Base Schemas

class SubscriptionBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=50, description="Subscription service name")
    total_slots: int = Field(..., ge=2, le=20, description="Total number of slots (2-20)")
    total_price: int = Field(..., gt=0, description="Total price in Naira")


class SubscriptionCreate(SubscriptionBase):
    """Schema for creating a new Subscription(admin only)"""
    pass

class SubscriptionUpdate(BaseModel):
    """Schema for updating Subscription, all fields optional"""
    name: Optional[str] = Field(None, min_length=2, max_length=50)
    total_slots: Optional[int] = Field(None, ge=2, le=20)
    total_price: Optional[int] = Field(None, gt=0)

# NESTED SCHEMAS (for groups within subscription)

class GroupInSubscription(BaseModel):
    """Minimal Group info shown when listing groups in subscription"""
    id: int
    subscription_id: int
    host_user_id: int
    slots_filled: int
    slots_available: int
    status: str
    renewal_date: datetime
    created_at: datetime

    class Config:
        from_attributes = True

# Response Schemas

class SubscriptionResponse(SubscriptionBase):
    """Basic subscription info (for list endpoint)"""
    id: int
    base_price_per_slot: int  # Your @property will provide this

    class Config:
        from_attributes = True


class SubscriptionDetailResponse(SubscriptionBase):
    """Detailed subscription info with available groups"""
    id: int
    base_price_per_slot: int
    available_groups: List[GroupInSubscription] = Field(default_factory=list)
    total_groups: int = 0

    class Config:
        from_attributes = True