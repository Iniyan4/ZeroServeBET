from django.urls import path
from .views import my_notifications, mark_read

urlpatterns = [
    path('', my_notifications),
    path('<int:notif_id>/read/', mark_read),
]