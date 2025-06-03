from rest_framework import serializers
from .models import WorkOrder
from django.utils import timezone

class WorkOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkOrder
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')

    def validate(self, data):
        # Add any custom validation logic here
        # if data['start_date'] > data['completion_date']:
        #     raise serializers.ValidationError("Completion date must be after start date")
        return data