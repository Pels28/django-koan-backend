from rest_framework import serializers
from .models import LandAcquisition

class LandAcquisitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = LandAcquisition
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
        
    def validate(self, data):
        # Add custom validation logic here
        if data['propertyType'] == 'land' and not data.get('landSize'):
            raise serializers.ValidationError("Land size is required for land properties")
        
        if data['propertyType'] == 'station' and not data.get('stationType'):
            raise serializers.ValidationError("Station type is required for station properties")
        
        return data