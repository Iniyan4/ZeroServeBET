from django.urls import path
from .views import (
    create_delivery,
    assign_partner,
    accept_delivery,
    update_status,
    my_tasks,
    delivery_detail
)

urlpatterns = [
    path('create/<int:claim_id>/', create_delivery),
    path('<int:task_id>/assign/', assign_partner),
    path('<int:task_id>/accept/', accept_delivery),
    path('<int:task_id>/status/', update_status),
    path('my/', my_tasks),
    path('<int:task_id>/', delivery_detail),
]