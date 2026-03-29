from django.urls import path
from .views import get_insights

urlpatterns = [
    # Map the root 'insights/' path directly to the get_insights function
    path('insights/', get_insights),
]