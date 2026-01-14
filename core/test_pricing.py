from datetime import date, timedelta
from core.pricing import (
    SubscriptionPlan,
    real_cost_per_slot,
    remaining_days,
    can_join,
    prorated_real_cost,
    platform_profit_per_user,
    join_price
)

def test_real_cost_per_slot():
    plan = SubscriptionPlan(
        name="Spotify Family",
        total_price=2500,
        total_slots=6,
        start_date=date.today(),
        renewal_date=date.today() + timedelta(days=30)
    )

    cost = real_cost_per_slot(plan)

    assert cost == 2500 / 6

def test_remaining_days():
    today = date.today()
    renewal_date = today + timedelta(days=10)

    plan = SubscriptionPlan(
        name="Spotify Family",
        total_price=2500,
        total_slots=6,
        start_date=today - timedelta(days=20),
        renewal_date=renewal_date
    )

    days_left = remaining_days(today, plan)
    assert days_left == 10

def test_can_join_within_15_days():
    today = date.today()
    start_date = today - timedelta(days=10)

    plan = SubscriptionPlan(
        name="Spotify Family",
        total_price=2500,
        total_slots=6,
        start_date=start_date,
        renewal_date=start_date + timedelta(days=30)
    )

    assert can_join(today, plan) is True


def test_cannot_join_after_15_days():
    today = date.today()
    start_date = today - timedelta(days=20)

    plan = SubscriptionPlan(
        name="Spotify Family",
        total_price=2500,
        total_slots=6,
        start_date=start_date,
        renewal_date=start_date + timedelta(days=30)
    )

    assert can_join(today, plan) is False


def test_cannot_join_after_15_days():
    today = date.today()
    start_date = today - timedelta(days=20)

    plan = SubscriptionPlan(
        name="Spotify Family",
        total_price=2500,
        total_slots=6,
        start_date=start_date,
        renewal_date=start_date + timedelta(days=30)
    )

    assert can_join(today, plan) is False


def test_platform_profit_rate_varies_by_subscription():
    plan = SubscriptionPlan(
        name="Apple music",
        total_price=1500,
        total_slots=6,
        start_date=date.today(),
        renewal_date=date.today() + timedelta(days=30)
    )

    profit = platform_profit_per_user(plan)
    print(profit)
    assert profit > 0
    assert profit < real_cost_per_slot(plan)


def test_join_price_returns_valid_result():
    today = date.today()

    plan = SubscriptionPlan(
        name="Netflix",
        total_price=8500,
        total_slots=4,
        start_date=today,
        renewal_date=today + timedelta(days=30)
    )

    result = join_price(today, plan)
    print(result)
    assert result.join_price > 0
    assert result.owner_credit > 0
    assert result.platform_profit > 0

if __name__ == "__main__":
    test_join_price_returns_valid_result()
    print("✓ test_join_price_returns_valid_result()")

