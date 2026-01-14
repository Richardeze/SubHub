SUBSCRIPTION_SLOT_RULES = {
    "spotify": {
        "total_slots": 6,
        "owner_reserved": 1
    },
    "netflix": {
        "total_slots": 4,
        "owner_reserved": 1
    },
    "apple music": {
        "total_slots": 6,
        "owner_reserved": 1
    },
    "youtube": {
        "total_slots": 6,
        "owner_reserved": 1
    }
}

def validate_subscription_slots(subscription_name: str, total_slots: int):
    rules = SUBSCRIPTION_SLOT_RULES.get(subscription_name.lower())

    # If we don’t enforce rules for this subscription, allow it
    if not rules:
        return

    if total_slots != rules["total_slots"]:
        raise ValueError(
            f"{subscription_name} requires exactly {rules['total_slots']} slots. "
            "You cannot use a plan already shared outside the platform."
        )