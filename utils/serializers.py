from uuid import uuid4
from django.utils import timezone
from django.db.models import Model
from rest_framework.fields import empty
from rest_framework.serializers import ModelSerializer as djangoModelSerializer
from .attr_handler import rsetattr

class ModelSerializer(djangoModelSerializer):

    class Meta:
        model = Model
        exclude = ['created_at', 'updated_at', 'id']

    def create(self, validated_data):
        if "id" not in validated_data:
            validated_data["id"] = str(uuid4())
        validated_data["created_at"] = timezone.now()
        validated_data["updated_at"] = timezone.now()
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.updated_at = timezone.now()
        return super().update(instance, validated_data)

def get_serializer(model, exclude=[], data=empty):
    model_serializer = ModelSerializer(data=data)
    rsetattr(model_serializer, 'Meta.model', model)
    model_serializer.Meta.exclude.extend(exclude)
    return model_serializer
