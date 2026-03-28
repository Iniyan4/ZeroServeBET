from datetime import datetime, timezone


def calculate_urgency(expiry_time, quantity):
    now = datetime.now(timezone.utc)

    time_left = (expiry_time - now).total_seconds() / 3600

    urgency = 100 - (time_left * 10)

    if quantity > 20:
        urgency += 10

    return max(0, min(100, urgency))