from  fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.subscription import Subscription
from models.group import Group
from models.user import User
from auth.dependencies import get_current_user, get_admin_user
from schemas.subscriptions import (
    SubscriptionCreate,
    SubscriptionUpdate,
    SubscriptionResponse,
    SubscriptionDetailResponse,
    GroupInSubscription
)

router = APIRouter(prefix="/subscriptions", tags=["Subscriptions"])
# Public Endpoint
@router.get("/", response_model=List[SubscriptionResponse])
def list_subscriptions(db:Session = Depends(get_db)):
    """
       List all available subscription plans.
       Shows basic info without groups.
       """
    subscriptions = db.query(Subscription).all()
    return subscriptions

@router.get("/{subscription_id}", response_model=SubscriptionDetailResponse)
def get_subscription_with_groups(
    subscription_id: int,
    db: Session = Depends(get_db)
):
    """
    Get detailed info about a subscription including all available groups.
    """

    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()

    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscription with ID {subscription_id} not found"
        )

    # Get all groups for this subscription
    groups = db.query(Group).filter(
        Group.subscription_id == subscription_id,
        Group.status == "open"
    ).all()

    formatted_groups = []

    for group in groups:
        formatted_groups.append({
            "id": group.id,
            "subscription_id": group.subscription_id,
            "host_user_id": group.host_user_id,
            "slots_filled": group.slots_filled,
            "slots_available": subscription.total_slots - group.slots_filled,
            "status": group.status,
            "renewal_date": group.renewal_date,
            "created_at": group.created_at
        })

    return {
        "id": subscription.id,
        "name": subscription.name,
        "total_slots": subscription.total_slots,
        "total_price": subscription.total_price,
        "base_price_per_slot": subscription.base_price_per_slot,
        "available_groups": formatted_groups,
        "total_groups": len(formatted_groups)
    }

# Admin Endpoints
@router.post("/", response_model=SubscriptionResponse, status_code=status.HTTP_201_CREATED)
def create_subscription( data: SubscriptionCreate,
                         db: Session = Depends(get_db),
                         admin: User = Depends(get_admin_user)):
    """
        Create a new subscription plan.
        Requires admin privileges.
        """
    # Check if subscription already exists
    existing = db.query(Subscription).filter(Subscription.name == data.name).first()

    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"'{data.name}' Subscription already exists")

    new_subscription = Subscription(name = data.name,
                                    total_price = data.total_price,
                                    total_slots = data.total_slots)
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)

    return new_subscription


@router.put("/{subscription_id}", response_model=SubscriptionResponse)
def update_subscription(
        subscription_id: int,
        data: SubscriptionUpdate,
        db: Session = Depends(get_db),
        admin: User = Depends(get_admin_user)
):
    """
    Update an existing subscription plan.
    Requires admin privileges.
    """
    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()

    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscription with ID {subscription_id} not found"
        )

    # Update only provided fields
    if data.name is not None:
        # Check for name conflicts
        existing = db.query(Subscription).filter(
            Subscription.name == data.name,
            Subscription.id != subscription_id
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Subscription name '{data.name}' already in use"
            )
        subscription.name = data.name

    if data.total_price is not None:
        subscription.total_price = data.total_price

    if data.total_slots is not None:
        subscription.total_slots = data.total_slots

    db.commit()
    db.refresh(subscription)

    return subscription


@router.delete("/{subscription_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_subscription(
        subscription_id: int,
        db: Session = Depends(get_db),
        admin: User = Depends(get_admin_user)
):
    """
    Delete a subscription plan.
    Requires admin privileges.

    WARNING: Cannot delete if there are active groups.
    """
    subscription = db.query(Subscription).filter(
        Subscription.id == subscription_id
    ).first()

    if not subscription:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Subscription with ID {subscription_id} not found"
        )

    # Safety check - don't delete if groups exist
    if subscription.groups:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cannot delete. {len(subscription.groups)} group(s) using this subscription."
        )

    db.delete(subscription)
    db.commit()

    return None