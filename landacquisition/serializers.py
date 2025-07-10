from rest_framework import serializers
from .models import LandAcquisition
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

class LandAcquisitionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    reviewed_by = UserSerializer(read_only=True, allow_null=True)
    review_date = serializers.DateTimeField(read_only=True)
    review_notes = serializers.CharField(allow_null=True, required=False)
    
    class Meta:
        model = LandAcquisition
        fields = '__all__'
        read_only_fields = (
            'user', 
            'created_at', 
            'updated_at',
            'reviewed_by',
            'review_date',
            'user,'
        )

    def validate(self, data):
        if data['propertyType'] == 'land' and not data.get('landSize'):
            raise serializers.ValidationError("Land size is required for land properties")
        
        if data['propertyType'] == 'station' and not data.get('stationType'):
            raise serializers.ValidationError("Station type is required for station properties")
        
        return data
    
    def create(self, validated_data):
        user = self.context['request'].user
        if user.is_manager:
            validated_data.update({
                'review_status': 'approved',
                'reviewed_by': user,
                'review_date': timezone.now()
            })
        return super().create(validated_data)