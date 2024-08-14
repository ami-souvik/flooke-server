from rest_framework.serializers import ModelSerializer, Serializer, BooleanField, CharField, IntegerField, FloatField,\
    URLField, EmailField, DateField, TimeField, ListField, DateTimeField
from transaction.models import TransactionModel, AccountModel, CategoryModel
from uuid import uuid4 as uuid


class SubAccountSerializer(ModelSerializer):
    class Meta:
        model = AccountModel
        exclude = ['created_at', 'updated_at', 'id']

class AccountSerializer(ModelSerializer):
    sub_accounts = SubAccountSerializer(many=True)

    class Meta:
        model = AccountModel
        exclude = ['created_at', 'updated_at','sub_accounts']

class SubCategorySerializer(ModelSerializer):
    class Meta:
        model = CategoryModel
        exclude = ['created_at', 'updated_at', 'id']

class CategorySerializer(Serializer):
    sub_categories = SubCategorySerializer(many=True)

    class Meta:
        model = CategoryModel
        exclude = ['created_at', 'updated_at', 'sub_categories']

class TxnCategorySerializer(CategorySerializer):
    sub_categories = SubCategorySerializer(many=False)

class TxnAccountSerializer(AccountSerializer):
    balance = FloatField(required=False)
    sub_accounts = SubAccountSerializer(many=False)

class TransactionSerializer(Serializer):
    class Meta:
        model = CategoryModel
        exclude = ['created_at', 'updated_at', 'id']
    
    def create(self, validated_data):
        validated_data["id"] = validated_data.get('id', str(uuid()))
        return TransactionModel(**validated_data)
    
    def update(self, instance, validated_data):
        instance.amount = validated_data.get('amount', instance.amount)
        instance.datetime = validated_data.get('datetime', instance.datetime)
        instance.category = validated_data.get('category', instance.category)
        instance.account = validated_data.get('account', instance.account)
        instance.save()
        return instance
