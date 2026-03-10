from sqlalchemy.orm import Session
from models.group_request import GroupRequest
from models.user import User

def get_pending_group_requests(
        *,
        db: Session,
        current_user: User
):
    if not current_user.is_admin:
        raise ValueError("Only admins can view group requests")

    requests = db.query(GroupRequest).filter(
        GroupRequest.status == "pending"
    ).all()

    return requests