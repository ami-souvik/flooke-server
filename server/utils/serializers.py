from uuid import uuid4
from datetime import datetime
from rest_framework.fields import empty
from rest_framework.serializers import ModelSerializer as djangoModelSerializer
from .attr_handler import rsetattr
from .models import Model

class ModelSerializer(djangoModelSerializer):

    class Meta:
        model = Model
        exclude = []

    def __init__(self, instance=None, data=empty, **kwargs):
        exclude = ['created_at', 'updated_at', 'id']
        if hasattr(self, 'Meta') and hasattr(self.Meta, 'exclude'):
            exclude.extend(self.Meta.exclude)
        self.Meta.exclude = exclude
        super().__init__(instance, data, **kwargs)

    def create(self, validated_data):
        validated_data["id"] = str(uuid4())
        validated_data["created_at"] = datetime.now()
        validated_data["updated_at"] = datetime.now()
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        instance.updated_at = datetime.now()
        return super().update(instance, validated_data)

def get_serializer(model, exclude=[], data=empty):
    model_serializer = ModelSerializer(data=data)
    rsetattr(model_serializer, 'Meta.model', model)
    rsetattr(model_serializer, 'Meta.exclude', exclude)
    return model_serializer
