from sqlalchemy.orm import Session
from models.group import Group
from datetime import datetime

def list_public_groups(db:Session):
    """ Returns all groups that are publicly joinable"""

    groups = db.query(Group).filter(
        Group.status == "open",
        Group.renewal_date > datetime.utcnow()
    ).all()

    return groups