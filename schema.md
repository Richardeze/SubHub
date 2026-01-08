# SubHub – Database Schema (Option A)

This schema is designed directly from your approved workflow and business rules.
We will keep it **clean, extensible, and FastAPI-friendly**.

---

## 1. users

Stores all platform users (owners + joiners).

```
users
-----
id (PK)
email (unique)
password_hash
full_name
role (user / admin)
created_at
updated_at
```

**Notes:**

* Same table for owners and joiners
* Role is optional but useful later

---

## 2. services

Represents Netflix, Spotify, etc.

```
services
--------
id (PK)
name (Netflix, Spotify, etc.)
max_slots
billing_cycle_days (usually 30)
created_at
```

**Why this exists:**

* Central place to enforce rules per service
* Prevents hardcoding values

---

## 3. subscriptions (owner’s original subscription)

Represents the subscription the owner already paid for externally.

```
subscriptions
-------------
id (PK)
owner_id (FK → users.id)
service_id (FK → services.id)
start_date
end_date
billing_cycle_days
proof_url
status (ACTIVE / INACTIVE / EXPIRED)
created_at
```

**Important:**

* This is NOT the shared plan yet
* This is what you verify

---

## 4. shared_plans

The actual plan users join.

```
shared_plans
------------
id (PK)
subscription_id (FK → subscriptions.id)
owner_id (FK → users.id)
service_id (FK → services.id)
plan_price
 total_slots
reserved_owner_slot (bool)
available_slots
status (ACTIVE / FULL / CANCELLED / EXPIRED)
created_at
```

**Rules:**

* available_slots = total_slots - 1 initially
* status changes drive most logic

---

## 5. plan_members

Tracks who joined which plan.

```
plan_members
------------
id (PK)
plan_id (FK → shared_plans.id)
user_id (FK → users.id)
joined_at
slot_number
status (ACTIVE / REFUNDED / REMOVED)
```

**Notes:**

* slot_number helps debugging
* Owner is NOT stored here

---

## 6. wallets

Separate wallets for owner payouts and platform.

```
wallets
-------
id (PK)
user_id (FK → users.id, nullable)
type (OWNER_PAYOUT / PLATFORM)
balance
locked_balance
created_at
```

**Rules:**

* Owners have locked_balance
* Platform wallet has no lock

---

## 7. transactions

Every money movement.

```
transactions
------------
id (PK)
user_id (FK → users.id)
plan_id (FK → shared_plans.id)
type (JOIN_PAYMENT / REFUND / PAYOUT)
amount
currency (NGN)
status (PENDING / SUCCESS / FAILED)
created_at
```

**Golden rule:**

* Wallets are DERIVED from transactions

---

## 8. billing_records

Stores proration and pricing details per join.

```
billing_records
---------------
id (PK)
user_id (FK → users.id)
plan_id (FK → shared_plans.id)
amount_paid
owner_part
platform_profit
proration_percentage
remaining_days
created_at
```

**Why this matters:**

* Auditable pricing
* Explains charges later

---

## 9. payout_rules (optional but recommended)

Stores configurable platform rules.

```
payout_rules
------------
id (PK)
min_remaining_percentage (e.g. 0.5)
platform_profit_percentage (e.g. 0.5)
payout_unlock_days_before_renewal (e.g. 3)
```

This avoids hardcoding business logic.

---

## Relationships Summary

```
users
 ├─ owns → subscriptions
 ├─ owns → shared_plans
 ├─ joins → plan_members
 └─ has → wallets

subscriptions
 └─ creates → shared_plans

shared_plans
 ├─ has → plan_members
 ├─ has → billing_records
 └─ has → transactions
```

---

## Status Flow (Important)

```
subscriptions: ACTIVE → INACTIVE → EXPIRED
shared_plans: ACTIVE → FULL → CANCELLED / EXPIRED
wallets: LOCKED → UNLOCKED
```

---
