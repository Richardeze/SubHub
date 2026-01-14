# This file contains ALL pricing, proration, owner payout, and platform profit logic.
from dataclasses import dataclass
from datetime import date

# CONSTANTS
DAYS_IN_CYCLE = 30
MIN_JOIN_DAYS = 15
PAYOUT_UNLOCK_DAYS = 3

# PROFIT RATES PER SUBSCRIPTION
PLATFORM_PROFIT_RATE = {
    "Spotify": 0.7,
    "Apple music": 1.5,
    "Netflix": 0.36,
    "Youtube": 0.7
}

# DATA MODELS
@dataclass
class SubscriptionPlan:
    name: str
    total_price: int       #e.g 2500
    total_slots: int       #e.g 6 including owner
    start_date: date
    renewal_date: date

@dataclass
class JoinResult:
    join_price: int
    owner_credit: int
    platform_profit: int

# CORE CALCULATIONS
# Calculate the real cost per slot (what the owner effectively paid per user)
def real_cost_per_slot(plan: SubscriptionPlan) -> float:
    return plan.total_price / plan.total_slots
    # Example: 2500 / 6 = ~416.67

# Calculate how many days remain in the subscription cycle
def remaining_days(today: date, plan: SubscriptionPlan) -> int:
    return max((plan.renewal_date - today).days, 0)

# Determine if joining is allowed based on your business rule
def can_join(today: date, plan: SubscriptionPlan) -> bool:
    days_used = DAYS_IN_CYCLE - remaining_days(today, plan)
    return days_used <= MIN_JOIN_DAYS

# Calculate prorated cost based ONLY on remaining days
def prorated_real_cost(today: date, plan: SubscriptionPlan) -> float:
    days_left = remaining_days(today,plan)
    per_day_cost = real_cost_per_slot(plan) / DAYS_IN_CYCLE
    return per_day_cost * days_left

# Platform profit is calculated based on the subscription as different subscription has their own rates
# 1. Get the subscription name so tha you can get the subscription rate for that subscription
def get_platfrom_profit_rate(plan: SubscriptionPlan) -> float:
    return PLATFORM_PROFIT_RATE.get(
        plan.name
    )

# 2. After getting the name, tap in to get the rate for that subscription to calculate what a user should pay
def platform_profit_per_user(plan: SubscriptionPlan) -> float:
    rate = get_platfrom_profit_rate(plan)
    if rate is None:
        raise ValueError(f"No platform profit rate defined for {plan.name}")
    return real_cost_per_slot(plan) * rate

# Final price a new User pays
def join_price(today: date, plan: SubscriptionPlan) -> JoinResult:
    if not can_join(today, plan):
        raise ValueError("Joining not allowed after 15 days from when Subscription starts")

    prorated_cost = prorated_real_cost(today, plan)
    platform_profit = platform_profit_per_user(plan)

    # What the new user pays
    final_price = prorated_cost + platform_profit

    # Owner only earns the prorated real cost (fairness rule)
    owner_credit = round(prorated_cost)
    return JoinResult(
        join_price=round(final_price),
        owner_credit=owner_credit,
        platform_profit=round(platform_profit)
    )

# OWNER'S PAYOUT UNLOCK LOGIC
def can_owner_withdraw(today: date, plan: SubscriptionPlan, slots_filled: int) -> bool:
    # First condition: All slots are filled
    if slots_filled >= plan.total_slots - 1: # Owner slot is the 1 excluded
        return True

    # Second condition: 3 days before Subscription renewal date
    if remaining_days(today,plan) <= PAYOUT_UNLOCK_DAYS:
        return True

    return False