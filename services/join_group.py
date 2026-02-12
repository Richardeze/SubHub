from datetime import date
from sqlalchemy.orm import Session

from models.group import Group
from models.group_member import GroupMember
from models.payment import Payment
from models.subscription import Subscription
from models.wallet import Wallet

from core.pricing import (SubscriptionPlan,
                          join_price)

def join_group(
        db: Session,
        user_id: int,
        group_id: int
):
    """ User joins an existing group and gets charged a prorated price"""

    # 1. Fetch Group
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise ValueError("Group not found")

    if group.status != "open":
        raise ValueError("This group is not open for joining")

    # 2. Prevent host from joining
    if group.host_user_id == user_id:
        raise ValueError("Host cannot join their own group")

    # 3. Prevent duplicate membership
    existing_member = db.query(GroupMember).filter(
        GroupMember.group_id == group_id,
        GroupMember.user_id == user_id
    ).first()
    if existing_member:
        raise ValueError("User already belongs to this group")

    # 4. Slot availability check
    if group.slots_filled >= group.subscription.total_slots:
        raise ValueError("Group is already full")

    # 5. Fetch Wallet
    user_wallet = db.query(Wallet).filter(Wallet.user_id == user_id).first()
    owner_wallet = db.query(Wallet).filter(Wallet.user_id == group.host_user_id).first()
    if not user_wallet or not owner_wallet:
         raise ValueError("Wallet not found")

    # 6. Build pricing plan
    subscription: Subscription = group.subscription
    plan = SubscriptionPlan(
        name = subscription.name,
        total_price= subscription.total_price,
        total_slots= subscription.total_slots,
        start_date=group.created_at.date(),
        renewal_date = group.renewal_date.date()
    )
    pricing_result = join_price(today=date.today(), plan=plan)

    # 7. Wallet Balance Check
    if user_wallet.available_balance < pricing_result.join_price:
        raise ValueError("Insufficient Wallet balance")

    # 8. Debit joiner / Credit Owner locked wallet
    user_wallet.available_balance -= pricing_result.join_price
    owner_wallet.locked_balance += pricing_result.owner_credit

    # 9. Create GroupMember
    member = GroupMember(
        group_id= group_id,
        user_id = user_id,
        payment_status = "paid",
        amount_paid = pricing_result.join_price,
    )
    db.add(member)

    # 10. Create Payment
    payment = Payment(
        payer_id= user_id,
        recipient_id = group.host_user_id,
        group_id = group_id,
        amount_paid = pricing_result.join_price,
        status = "successful",
        payment_purpose = "join_payment",
        payment_method = "wallet"
    )
    db.add(payment)

    # 11. Update group slots
    group.slots_filled += 1
    if group.slots_filled >= subscription.total_slots:
        group.status = "full"

    db.commit()
    db.refresh(member)

    return {
        "group_id": group.id,
        "join_price": pricing_result.join_price,
        "owner_credit": pricing_result.owner_credit,
        "platform_profit": pricing_result.platform_profit,
        "wallet_balance": user_wallet.available_balance
    }