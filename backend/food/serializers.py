from rest_framework import serializers
from .models import FoodListing


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodListing
        fields = '__all__'
        read_only_fields = ['donor', 'expiry_time', 'urgency_score']