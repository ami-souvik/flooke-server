from django.utils import timezone
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import User

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ['created_at', 'updated_at']

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.updated_at = timezone.now()
        return super().update(instance, validated_data)

class ObtainTokenSerializer(TokenObtainPairSerializer):
    pass
