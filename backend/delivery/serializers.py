from rest_framework import serializers
from .models import DeliveryTask


class DeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryTask
        fields = '__all__'
        read_only_fields = ['status']