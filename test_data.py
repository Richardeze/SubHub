from database import SessionLocal
from models.user import User
from models.group import Group
db = SessionLocal()

test_user = User(
    email="testuser@example.com",
    full_name="Test User"
)

plan = Group(
    name="Netflix Premium",
    price=8000,
    total_slots=4
)

db.add(plan)
db.add(test_user)
db.commit()
db.refresh(plan)
db.refresh(test_user)
db.close()


print("Inserted plan with ID:", plan.id)
print("Inserted user with ID", test_user.id)