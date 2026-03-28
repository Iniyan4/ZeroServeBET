from django.urls import path
from .views import create_food, list_food, food_detail, cancel_food

urlpatterns = [
    path('', list_food),
    path('create/', create_food),
    path('<int:food_id>/', food_detail),
    path('<int:food_id>/cancel/', cancel_food),
]