from database import SessionLocal, engine
from models.base import Base
from models.user import User
from models.subscription import Subscription
from models.group import Group
from models.group_member import GroupMember
from models.group_request import GroupRequest
from models.wallet import Wallet
from models.payment import Payment
from datetime import datetime, timedelta
from auth.hashing import hash_password

# ✅ ADD THIS SECTION - Create all tables first
print("📦 Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✅ Tables created!")

# NOW create the session
db = SessionLocal()
try:
    print("🌱 Seeding database with test data...")

    # ===== 1. CREATE USERS =====
    print("Creating users...")

    user1 = User(
        email="host@example.com",
        hashed_password=hash_password("password123"),  # Host user
        is_active=True
    )
    user2 = User(
        email="joiner@example.com",
        hashed_password=hash_password("password123"),  # Joiner user
        is_active=True
    )

    db.add(user1)
    db.add(user2)
    db.commit()
    db.refresh(user1)
    db.refresh(user2)
    print(f"✅ Created user1 (host) with ID: {user1.id}")
    print(f"✅ Created user2 (joiner) with ID: {user2.id}")

    # ===== 2. CREATE WALLETS =====
    print("Creating wallets...")

    # Host wallet - starts with some balance
    wallet1 = Wallet(
        user_id=user1.id,
        available_balance=5000,  # ₦5000
        locked_balance=0
    )

    # Joiner wallet - needs enough to pay for subscription slot
    wallet2 = Wallet(
        user_id=user2.id,
        available_balance=10000,  # ₦10000
        locked_balance=0
    )
    db.add(wallet1)
    db.add(wallet2)
    db.commit()
    db.refresh(wallet1)
    db.refresh(wallet2)
    print(f"✅ Created wallet for host (balance: ₦{wallet1.available_balance})")
    print(f"✅ Created wallet for joiner (balance: ₦{wallet2.available_balance})")

    # ===== 3. CREATE SUBSCRIPTIONS =====
    print("Creating subscriptions...")

    netflix = Subscription(
        name="Netflix",
        total_price=8500,   # ₦8500 total for family plan
        total_slots=4,      # 4 slots
    )

    spotify = Subscription(
        name="Spotify",
        total_price=2500,   # ₦2500 total for family plan
        total_slots=6,  # 6 slots
    )

    apple_music = Subscription(
        name="Apple Music",
        total_price=1800,   # ₦1800 total
        total_slots=6,      # 6 slots
    )

    youtube = Subscription(
        name="Youtube",
        total_price=2800, # ₦2800 total
        total_slots=6,  # 6 slots
    )
    db.add(netflix)
    db.add(spotify)
    db.add(apple_music)
    db.add(youtube)
    db.commit()
    db.refresh(netflix)
    db.refresh(spotify)
    db.refresh(apple_music)
    db.refresh(youtube)
    print(f"✅ Created Netflix subscription (ID: {netflix.id})")
    print(f"✅ Created Spotify subscription (ID: {spotify.id})")
    print(f"✅ Created Apple Music subscription (ID: {apple_music.id})")
    print(f"✅ Created Youtube subscription (ID: {youtube.id})")

    # ===== 4. CREATE GROUP REQUESTS =====
    print("Creating group requests...")
    # Calculate dates
    today = datetime.now()
    start_date = today
    end_date = today + timedelta(days=30)

    netflix_request = GroupRequest(
        requester_id=user1.id,
        subscription_id=netflix.id,
        total_slots=4,
        sub_start_date=start_date,
        sub_end_date=end_date,
        renewal_date=end_date,
        payment_method="wallet",
        status="pending"
    )

    spotify_request = GroupRequest(
        requester_id=user1.id,
        subscription_id=spotify.id,
        total_slots=6,
        sub_start_date=start_date,
        sub_end_date=end_date,
        renewal_date=end_date,
        payment_method="wallet",
        status="pending"
    )

    db.add(netflix_request)
    db.add(spotify_request)
    db.commit()
    db.refresh(netflix_request)
    db.refresh(spotify_request)
    print(f"✅ Created Netflix group request (ID: {netflix_request.id})")
    print(f"✅ Created Spotify group request (ID: {spotify_request.id})")

    # ===== 5. CREATE AN ALREADY APPROVED GROUP =====
    # (So we can test joining immediately)
    print("Creating an open group for testing joins...")

    open_group = Group(
        subscription_id=netflix.id,
        host_user_id=user1.id,
        slots_filled=1,
        status="open",
        created_at=start_date,
        renewal_date=datetime.utcnow() + timedelta(days=30)
    )

    db.add(open_group)
    db.commit()
    db.refresh(open_group)
    print(f"✅ Created open Netflix group (ID: {open_group.id})")

    # ===== SUMMARY =====
    print("\n" + "="*50)
    print("✅ DATABASE SEEDED SUCCESSFULLY!")
    print("="*50)
    print(f"Users created:        2 (IDs: {user1.id}, {user2.id})")
    print(f"Wallets created:      2")
    print(f"Subscriptions:        4 (Netflix, Spotify, Apple Music, Youtube)")
    print(f"Group Requests:       2 (IDs: {netflix_request.id}, {spotify_request.id})")
    print(f"Open Groups:          1 (ID: {open_group.id})")
    print("="*50)
    print("\n📝 USE THESE IDs FOR TESTING:")
    print(f"Host user_id:         {user1.id}")
    print(f"Joiner user_id:       {user2.id}")
    print(f"Netflix sub_id:       {netflix.id}")
    print(f"Open group_id:        {open_group.id}")
    print(f"Netflix request_id:   {netflix_request.id}")
    print(f"Spotify request_id:   {spotify_request.id}")

except Exception as e:
    print(f"❌ Error seeding database: {e}")
    db.rollback()

finally:
    db.close()

