from database import engine
from models.base import Base
from models.user import User
from models.payment import Payment
from models.subscription import Subscription
from models.group import Group
from models.group_member import GroupMember
from models.group_request import GroupRequest
from models.wallet import Wallet
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully")