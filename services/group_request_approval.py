from sqlalchemy.orm import Session
from models.group_request import GroupRequest
from models.group import Group
from models.subscription import Subscription
from core.subscription_rules import validate_subscription_slots

def approve_group_request(
        db: Session,
        group_request_id: int,
):
    """ Approves a pending GroupRequest and creates a Group"""
    # 1. Fetch the GroupRequest
    group_request = db.query(GroupRequest).filter(
        GroupRequest.id == group_request_id
    ).first()
    if not group_request:
        raise ValueError("Group request not found")

    if group_request.status != "pending":
        raise ValueError("Only pending requests can be approved")

    # 2. Fetch Subscription (extra safety)
    subscription = db.query(Subscription).filter(
        Subscription.id == group_request.subscription_id
    ).first()
    if not subscription:
        raise ValueError("Associated subscription not found")

    # 3. Enforce platform slot rules (FINAL GATE)
    validate_subscription_slots(
        subscription_name=subscription.name,
        total_slots=group_request.total_slots
    )

    # 4. Create the group
    group = Group(
        subscription_id = group_request.subscription.id,
        host_user_id = group_request.requester_id,
        slots_filled = 1,
        status = "open",
        renewal_date = group_request.renewal_date
    )

    # 4. Update the Group request status
    group_request.status = "approved"

    # 5. Persist changes
    db.add(group)
    db.commit()
    db.refresh(group)

    return group