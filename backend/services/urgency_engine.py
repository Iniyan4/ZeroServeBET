# backend/services/urgency_engine.py
from django.utils import timezone

def calculate_urgency(food_listing):
    now = timezone.now()
    age_hours = (now - food_listing.prepared_at).total_seconds() / 3600

    # Higher score for older food (prepared earlier)
    score = min(100, age_hours * 10)
    return round(score, 2)