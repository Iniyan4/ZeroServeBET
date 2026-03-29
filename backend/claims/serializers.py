from rest_framework import serializers

from delivery.models import DeliveryTask
from .models import Claim


class ClaimSerializer(serializers.ModelSerializer):
    ngo_username = serializers.CharField(source='ngo.username', read_only=True)
    delivery_status = serializers.SerializerMethodField()

    class Meta:
        model = Claim
        fields = '__all__'


    def get_delivery_status(self, obj):
        # Find the delivery task associated with this claim
        task = DeliveryTask.objects.filter(claim=obj).first()
        return task.status if task else None