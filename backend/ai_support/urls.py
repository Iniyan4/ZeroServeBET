from django.urls import path
from .views import (
    ai_review_user,
    ai_review_food,
    ai_complaint_summary,
    admin_ai_insight
)

urlpatterns = [
    path('review-user/', ai_review_user),
    path('review-food/', ai_review_food),
    path('complaint-summary/', ai_complaint_summary),
    path('admin-insight/', admin_ai_insight),
]