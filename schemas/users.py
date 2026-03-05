from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

# USER SCHEMAS
class UserResponse(BaseModel):
    """Public user info (no password)"""
    id: int
    email: EmailStr
    is_active: bool
    is_admin: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Wallet schemas
class WalletResponse(BaseModel):
    """User's wallet information"""
    id: int
    user_id: int
    available_balance: int
    locked_balance: int
    total_balance: int  # We'll calculate this
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class FundWalletRequest(BaseModel):
    """Request to add money to wallet"""
    amount: int  # Amount in Naira (or kobo)
    payment_method: str = "mock_payment"  # For now, just mock

# Payment Schemas
class PaymentResponse(BaseModel):
    id: int
    amount_paid: int
    status: str
    payment_purpose: str
    payment_type: str
    transaction_type: str
    group_id: int | None
    reference: str | None
    created_at: datetime

    class Config:
        orm_mode = True


class PaymentHistoryResponse(BaseModel):
    wallet_balance: int
    count: int
    payments: List[PaymentResponse]
