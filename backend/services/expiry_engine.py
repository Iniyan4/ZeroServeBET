from datetime import timedelta


def calculate_expiry(food_category, prepared_at):
    rules = {
        "cooked": 4,
        "bakery": 8,
        "packed": 24,
    }

    hours = rules.get(food_category, 4)
    return prepared_at + timedelta(hours=hours)