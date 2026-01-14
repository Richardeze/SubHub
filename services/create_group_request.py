from typing import Optional
from sqlalchemy.orm import Session
from models.group_request import GroupRequest
from models.subscription import Subscription
from datetime import datetime, date
from core.subscription_rules import validate_subscription_slots

def create_group_request(db: Session,
                         requester_id: int,
                         subscription_id: int,
                         sub_start_date: datetime,
                         sub_end_date: datetime,
                         renewal_date: datetime,
                         total_slots: int,
                         payment_method: str,
                         card_expiry: Optional[date],
                         proof_url: str | None = None
                         ):

    """ 1. Validate Subscription exists"""
    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()
    if not subscription:
        raise ValueError("Subscription does not exist")

    """ 2. Enforce subscription slot rules """
    validate_subscription_slots(
        subscription_name=subscription.name,
        total_slots=total_slots
    )
    """ 3. Date Validation"""
    if not (sub_start_date < renewal_date <= sub_end_date):
        raise ValueError("Invalid Subscription dates")

    """ 4. Prevent duplicate pending group requests"""
    existing_group_request = (db.query(GroupRequest).filter(
        GroupRequest.requester_id == requester_id,
        GroupRequest.subscription_id == subscription_id,
        GroupRequest.status == "pending"
    )).first()
    if existing_group_request:
        raise ValueError("You already have a pending request for this subscription")

    """ Card expiry validation"""
    if payment_method == "card" and not card_expiry:
        raise ValueError("Card expiry is required when payment method is card")

    """ 5. Create GroupRequest"""
    group_request = GroupRequest(
        requester_id = requester_id,
        subscription_id = subscription_id,
        sub_start_date = sub_start_date,
        sub_end_date=sub_end_date,
        renewal_date=renewal_date,
        total_slots = total_slots,
        payment_method = payment_method,
        card_expiry = card_expiry,
        proof_url = proof_url,
        status="pending"
    )
    db.add(group_request)
    db.commit()
    db.refresh(group_request)

    return group_request