from rest_framework import serializers
from .models import WorkOrder
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name']

class WorkOrderSerializer(serializers.ModelSerializer):
    requester = serializers.ChoiceField(
        choices=WorkOrder.DEPARTMENT_CHOICES
    )
    user = UserSerializer(read_only=True)
    # Add the new fields to the serializer
    review_status = serializers.CharField(read_only=True)
    reviewed_by = UserSerializer(read_only=True, allow_null=True)
    review_date = serializers.DateTimeField(read_only=True)
    review_notes = serializers.CharField(
        allow_null=True, 
        required=False
    )

    class Meta:
        model = WorkOrder
        fields = '__all__'
        read_only_fields = (
            'user', 
            'created_at', 
            'updated_at', 
            'work_order_number',
            'is_approved',
    
            'reviewed_by',
            'review_date',
            'user',
        )

    def validate(self, data):
        # Add any custom validation logic here
        # if data['start_date'] > data['completion_date']:
        #     raise serializers.ValidationError("Completion date must be after start date")
        return data

    def create(self, validated_data):
        # Get the current user
        user = self.context['request'].user
        
        # If user is manager, set review status to approved
        if user.is_manager:
            validated_data.update({
                'review_status': 'approved',
                'reviewed_by': user,
                'review_date': timezone.now(),
                'is_approved': True
            })
        
        return super().create(validated_data)