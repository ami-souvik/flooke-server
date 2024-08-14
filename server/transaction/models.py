import os
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, UTCDateTimeAttribute, JSONAttribute
from utils.env_handler import get_dynamodb_conf

db_conf = get_dynamodb_conf()

class TransactionModel(Model):
    class Meta:
        table_name = 'Transaction'
        region = db_conf["region"]
        host = db_conf["host"]
        write_capacity_units = 1
        read_capacity_units = 1

    user_id = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute(range_key=True)
    amount = NumberAttribute()
    datetime = UTCDateTimeAttribute()
    category = JSONAttribute()
    account = JSONAttribute()
    created_at = UTCDateTimeAttribute()
    updated_at = UTCDateTimeAttribute()

    def to_dict(self):
        return self.attribute_values


class CategoryModel(Model):
    class Meta:
        table_name = 'Category'
        region = db_conf["region"]
        host = db_conf["host"]
        write_capacity_units = 1
        read_capacity_units = 1

    user_id = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute(range_key=True)
    sub_categories = JSONAttribute()
    created_at = UTCDateTimeAttribute()
    updated_at = UTCDateTimeAttribute()

    def to_dict(self):
        return self.attribute_values


class AccountModel(Model):
    class Meta:
        table_name = 'Account'
        region = db_conf["region"]
        host = db_conf["host"]
        write_capacity_units = 1
        read_capacity_units = 1

    user_id = UnicodeAttribute(hash_key=True)
    id = UnicodeAttribute(range_key=True)
    name = UnicodeAttribute()
    sub_accounts = JSONAttribute()
    created_at = UTCDateTimeAttribute()
    updated_at = UTCDateTimeAttribute()

    def to_dict(self):
        return self.attribute_values
