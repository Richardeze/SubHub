from models.payment import Payment
import uuid
from datetime import datetime
from fastapi import HTTPException, status

def create_payment(
    db,
    payer_id: int,
    amount: int,
    purpose: str,
    payment_type: str,
    group_id: int = None,
    payment_status: str = "completed"
):
    # Generate a unique payment reference
    reference = f"PAY-{datetime.utcnow().strftime('%Y%m%d')}-{uuid.uuid4().hex[:10].upper()}"

    payment = Payment(
        payer_id=payer_id,
        group_id=group_id,
        amount_paid=amount,
        status=payment_status,
        payment_purpose=purpose,
        payment_type=payment_type,
        reference=reference
    )

    db.add(payment)
    db.flush()
    return payment