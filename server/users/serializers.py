from uuid import uuid4
from datetime import datetime
from rest_framework.serializers import ModelSerializer
from .models import Persona

class UserSerializer(ModelSerializer):

    class Meta:
        model = Persona
        exclude = ['created_at', 'updated_at', 'id']

    def create(self, validated_data):
        validated_data["id"] = str(uuid4())
        validated_data["created_at"] = datetime.now()
        validated_data["updated_at"] = datetime.now()
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.updated_at = datetime.now()
        return super().update(instance, validated_data)
