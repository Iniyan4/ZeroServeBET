from django.urls import path
from .views import (
    admin_analytics,
    donor_analytics,
    ngo_analytics,
    delivery_analytics,
    impact_metrics
)

urlpatterns = [
    path('admin/', admin_analytics),
    path('donor/', donor_analytics),
    path('ngo/', ngo_analytics),
    path('delivery/', delivery_analytics),
    path('impact/', impact_metrics),
]