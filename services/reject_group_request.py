from sqlalchemy.orm import Session
from models.group_request import GroupRequest
from models.subscription import Subscription
from models.user import User
from core.subscription_rules import validate_subscription_slots

def reject_group_request(
    *,
    db: Session,
    group_request_id: int,
    rejection_reason: str,
    current_user: User
):
    """
    Reject a pending group request with a reason
    """
    # 1. ADMIN PROTECTION (BUSINESS RULE)
    if not current_user.is_admin:
        raise ValueError("Only Admin can reject group requests")
    # 2. Fetch the group request
    group_request = db.query(GroupRequest).filter(
        GroupRequest.id == group_request_id
    ).first()

    if not group_request:
        raise ValueError("Group request not found")

    # 3. Ensure it's still pending
    if group_request.status != "pending":
        raise ValueError("Group request has already been processed")

    # 4. Fetch subscription (for rule validation)
    subscription = db.query(Subscription).filter(
        Subscription.id == group_request.subscription_id
    ).first()

    if not subscription:
        raise ValueError("Subscription linked to this request does not exist")

    # 5. Slot rule enforcement (defensive)
    try:
        validate_subscription_slots(
            subscription_name=subscription.name,
            total_slots=group_request.total_slots
        )
    except ValueError as e:
        # If rule fails, overwrite reason with system-enforced reason
        rejection_reason = str(e)

    # 6. Reject the request
    group_request.status = "rejected"
    group_request.rejection_reason = rejection_reason

    db.commit()
    db.refresh(group_request)

    return group_request