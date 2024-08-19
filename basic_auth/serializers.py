from datetime import datetime
from django.contrib.auth.hashers import make_password
from rest_framework.serializers import ModelSerializer
from .models import User

class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        exclude = ['created_at', 'updated_at']

    def create(self, validated_data):
        validated_data["password"] = make_password(validated_data["password"])
        validated_data["created_at"] = datetime.now()
        validated_data["updated_at"] = datetime.now()
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.updated_at = datetime.now()
        return super().update(instance, validated_data)
