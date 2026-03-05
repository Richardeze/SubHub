from fastapi import FastAPI
from  database import engine, Base
# Models imports
from models.base import Base
from models.user import User
from models.subscription import Subscription
from models.group import Group
from models.group_member import GroupMember
from models.group_request import GroupRequest
from models.wallet import Wallet
from models.payment import Payment

# Router imports
from routers import groups, auth, subscriptions, users

# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SubHub - Subscription Sharing Platform",
    description="Platform for sharing family subscription plans",
    version="1.0.0"
)

app.include_router(groups.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(subscriptions.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "message": "Subscription Sharing API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}