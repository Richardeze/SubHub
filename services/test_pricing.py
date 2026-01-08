from datetime import date
from services.pricing import (
    SubscriptionPlan,
    JoinResult,
    can_owner_withdraw,
    join_price,
    real_cost_per_slot
)
plan = SubscriptionPlan(
    total_price= 2500,
    total_slots= 6,
    start_date= date(2025, 1,1),
    renewal_date= date(2025, 1, 31)
)
today = date(2025, 1, 26)
#result = join_price(today, plan)
slots_filled = 4
can_withdraw = can_owner_withdraw(today, plan, slots_filled)

print("LAST DAY ALLOWED JOIN")
#print("User pays:", result.join_price)
#print("Owner earns:", result.owner_credit)
#print("Platform gains:", result.platform_profit)
print("Normal slot price for each user:", real_cost_per_slot(plan))
print("-" * 30)
print("Can owner withdraw?", can_withdraw)