from models.payment import Payment
from models.wallet import Wallet
from fastapi import HTTPException, status

def create_payment(
    db,
    payer_id: int,
    amount: int,
    purpose: str,
    payment_type: str,
    group_id: int = None,
    status: str = "completed",
    reference: str = None
):
    payment = Payment(
        payer_id=payer_id,
        group_id=group_id,
        amount_paid=amount,
        status=status,
        payment_purpose=purpose,
        payment_type=payment_type,
        reference=reference
    )

    db.add(payment)
    return payment