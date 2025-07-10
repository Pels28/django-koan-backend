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
        token["is_manager"] = user.is_manager
        return token
    
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    is_manager = serializers.BooleanField(required=False, default=False)  # Optional field for registration

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "password", "is_manager"]
        
    def create(self, validated_data):
        user = User.objects.create(
            email = validated_data["email"],
            first_name = validated_data["first_name"],
            last_name = validated_data["last_name"],
            is_manager = validated_data.get("is_manager", False)  # Set manager status
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
    is_manager = serializers.BooleanField()

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "is_manager", "profile"]
        
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])

    class Meta:
        fields = ['old_password', 'new_password']
    
    
    