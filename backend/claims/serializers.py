from rest_framework import serializers
from .models import Claim


class ClaimSerializer(serializers.ModelSerializer):
    ngo_username = serializers.CharField(source='ngo.username', read_only=True)

    class Meta:
        model = Claim
        fields = '__all__'