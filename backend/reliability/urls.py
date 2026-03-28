from django.urls import path
from .views import (
    get_reliability,
    add_violation,
    set_restriction,
    list_violations
)

urlpatterns = [
    path('<int:user_id>/', get_reliability),
    path('violations/add/', add_violation),
    path('violations/<int:user_id>/', list_violations),
    path('admin/restrict/', set_restriction),
]