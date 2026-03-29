from rest_framework import serializers
from .models import DeliveryTask


class DeliverySerializer(serializers.ModelSerializer):
    claim_status = serializers.CharField(source='claim.status', read_only=True)
    class Meta:
        model = DeliveryTask
        fields = '__all__'