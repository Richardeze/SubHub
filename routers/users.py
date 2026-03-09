from fastapi import APIRouter, HTTPException, Depends, status, Query
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.user import User
from models.wallet import Wallet
from models.payment import Payment
from services.payment_service import create_payment
from auth.dependencies import get_current_user
from schemas.users import *

router = APIRouter(prefix="/users", tags=["Users & Wallets"])

# User profile endpoint
@router.get("/me", response_model=UserResponse)
def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current logged-in user's profile
       Requires authentication"""
    return current_user

# Wallet endpoints
@router.get("/me/wallet", response_model=WalletResponse)
def get_user_wallet(current_user: User = Depends(get_current_user),
                    db: Session = Depends(get_db)):
    """Get current user wallet balance.
       Shows available balance, locked balance and total"""
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()

    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Wallet not found, Please contact support.")

    # Calculate total balance
    total = wallet.available_balance + wallet.locked_balance

    return WalletResponse(
        id=wallet.id,
        user_id=wallet.user_id,
        available_balance=wallet.available_balance,
        locked_balance=wallet.locked_balance,
        total_balance=wallet.available_balance + wallet.locked_balance,
        created_at=wallet.created_at,
        updated_at=wallet.updated_at
    )

@router.post("/me/wallet/fund", response_model=FundWalletResponse)
def fund_wallet(
        request: FundWalletRequest,
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)):
    """ Add money to wallet (Mock payment for testing now)
        PRODUCTION TODO:
    - Integrate Korapay payment gateway
    - Verify payment before crediting wallet
    - Add webhook endpoint for payment confirmation"""
    if request.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail= "Amount must be greater than zero")

    if request.amount > 1000000:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail= "Maximum funding amount is 1,000,000")

    # Get wallet
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()

    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= "Wallet not found")

    # Add money (MOCK - in production, verify payment first!)
    old_balance = wallet.available_balance
    wallet.available_balance += request.amount

    # Create Payment record
    create_payment(
        db=db,
        payer_id=current_user.id,
        amount=request.amount,
        purpose="wallet_funding",
        payment_type=request.payment_method,
        status="completed"
    )

    db.commit()
    db.refresh(wallet)

    return {
        "success": True,
        "message": f"Successfully added ₦{request.amount:,} to your wallet",
        "previous_balance": old_balance,
        "amount_added": request.amount,
        "new_balance": wallet.available_balance,
        "payment_method": request.payment_method
    }

# Payment history endpoints
@router.get("/me/payments", response_model= PaymentHistoryResponse)
def get_payment_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = Query(20, le=100),
    offset: int = Query(0, ge=0),
    status: str | None = None,
    purpose: str | None = None
):
    """
    Get current user's payment history.
    Supports filtering and pagination.
    """

    query = db.query(Payment).filter(
        Payment.payer_id == current_user.id
    )

    if status:
        query = query.filter(Payment.status == status)

    if purpose:
        query = query.filter(Payment.payment_purpose == purpose)

    payments = (
        query.order_by(Payment.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )

    payment_list = []

    for payment in payments:
        if payment.payment_purpose in ["Wallet_funding", "Refund"]:
            transaction_type = "credit"
        else:
            transaction_type = "debit"

        payment_list.append({
            "id": payment.id,
            "amount_paid": payment.amount_paid,
            "status": payment.status,
            "payment_purpose": payment.payment_purpose,
            "payment_type": payment.payment_type,
            "group_id": payment.group_id,
            "reference": payment.reference,
            "created_at": payment.created_at,
            "transaction_type": transaction_type
        })

    # Get wallet balance properly
    wallet = db.query(Wallet).filter(
        Wallet.user_id == current_user.id
    ).first()

    wallet_balance = wallet.available_balance if wallet else 0

    return {
        "wallet_balance": wallet_balance,
        "count": len(payment_list),
        "payments": payment_list
    }