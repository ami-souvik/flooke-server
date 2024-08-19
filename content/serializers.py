from uuid import uuid4
from datetime import datetime
from rest_framework.serializers import ModelSerializer
from .models import Content

class ContentSerializer(ModelSerializer):

    class Meta:
        model = Content
        exclude = ['created_at', 'updated_at','owner']

    def create(self, validated_data):
        validated_data["created_at"] = datetime.now()
        validated_data["updated_at"] = datetime.now()
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.updated_at = datetime.now()
        return super().update(instance, validated_data)
