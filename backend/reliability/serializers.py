from rest_framework import serializers
from .models import Reliability, Violation


class ReliabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reliability
        fields = '__all__'


class ViolationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Violation
        fields = '__all__'
        read_only_fields = ['action_taken']