from rest_framework.serializers import Serializer, BooleanField, CharField, IntegerField, FloatField,\
    URLField, EmailField, DateField, TimeField, ListField
from transaction.models import TransactionModel

class Transaction(Serializer):
    txn_id = CharField(required=True)
    amount = FloatField(required=True)

    def create(self, validated_data):
        return TransactionModel(**validated_data)
