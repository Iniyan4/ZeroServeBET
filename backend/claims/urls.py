from django.urls import path
from .views import (
    create_claim,
    accept_claim,
    reject_claim,
    my_claims,
    food_claims
)

urlpatterns = [
    path('create/<int:food_id>/', create_claim),
    path('<int:claim_id>/accept/', accept_claim),
    path('<int:claim_id>/reject/', reject_claim),
    path('my/', my_claims),
    path('food/<int:food_id>/', food_claims),
]