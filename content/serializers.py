from django.utils import timezone
from rest_framework.serializers import ModelSerializer
from .models import Content

class ContentSerializer(ModelSerializer):

    class Meta:
        model = Content
        exclude = ['created_at', 'updated_at']

    def create(self, validated_data):
        validated_data["created_at"] = timezone.now()
        validated_data["updated_at"] = timezone.now()
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.updated_at = timezone.now()
        return super().update(instance, validated_data)
