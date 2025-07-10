# serializers.py
from rest_framework import serializers
from .models import LandAcquisition
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'full_name']

class LandAcquisitionSerializer(serializers.ModelSerializer):
    # Add review fields to serializer
    review_status = serializers.CharField(read_only=True)
    user = UserSerializer(read_only=True)
    reviewed_by = UserSerializer(read_only=True, allow_null=True)
    review_date = serializers.DateTimeField(read_only=True)
    review_notes = serializers.CharField(
        allow_null=True, 
        required=False
    )
    
    class Meta:
        model = LandAcquisition
        fields = '__all__'
        read_only_fields = (
            'user', 
            'created_at', 
            'updated_at',
            'reviewed_by',
            'review_date',
            'review_status',
            'user,'
        )

    def validate(self, data):
        # Existing validation logic
        if data['propertyType'] == 'land' and not data.get('landSize'):
            raise serializers.ValidationError("Land size is required for land properties")
        
        if data['propertyType'] == 'station' and not data.get('stationType'):
            raise serializers.ValidationError("Station type is required for station properties")
        
        return data