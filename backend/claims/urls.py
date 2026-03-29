from django.urls import path
from .views import (
    create_claim,
    accept_claim,
    reject_claim,
    my_claims,
    food_claims, verify_delivery, dispute_delivery
)

urlpatterns = [
    path('create/<int:food_id>/', create_claim),
    path('<int:claim_id>/accept/', accept_claim),
    path('<int:claim_id>/reject/', reject_claim),
    path('my/', my_claims),
    path('food/<int:food_id>/', food_claims),
    path('<int:claim_id>/verify/', verify_delivery),
    path('<int:claim_id>/dispute/', dispute_delivery),
]