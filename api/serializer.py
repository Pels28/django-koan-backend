from .models import User, Profile
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ["id", "email", "first_name", "last_name", ]


        
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["full_name"] = user.profile.full_name
        token["email"] = user.email
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["bio"] = user.profile.bio
        token["image"] = str(user.profile.image.url)
        token["verified"] = user.profile.verified
        return token
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password ])
    
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "password"]
        
    def validate(self, attrs):
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(
            email = validated_data["email"],
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"]
        )
        
        user.set_password(validated_data["password"])
        user.save()
        
        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['full_name', 'bio', 'image', 'verified']
        read_only_fields = ['image'] 
        
class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "profile"]
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    class Meta:
        fields = ['old_password', 'new_password']
    
    
    