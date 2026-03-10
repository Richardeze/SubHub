from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional


class CreateGroupRequest(BaseModel):
    subscription_name: str = Field(..., min_length=2, max_length=50)

    sub_start_date: datetime
    sub_end_date: datetime
    renewal_date: datetime

    total_slots: int = Field(..., ge=2, le=20)

    payment_method: str = Field(..., pattern="^(card|transfer)$")

    card_expiry: Optional[date] = None

    proof_url: Optional[str] = None

class RejectGroupRequest(BaseModel):
    rejection_reason: str