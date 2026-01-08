from database import engine
from models.base import Base
from models.user import User
from models.payment import Payment
from models.subscription_plan import SubscriptionPlan
from models.subscription_slot import SubscriptionSlot
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("All tables created successfully")