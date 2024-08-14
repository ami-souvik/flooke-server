import os
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute
from utils.env_handler import get_dynamodb_conf

db_conf = get_dynamodb_conf()

class TransactionModel(Model):
    class Meta:
        table_name = 'Transaction'
        # Specifies the region
        region = db_conf["region"]
        # Optional: Specify the hostname only if it needs to be changed from the default AWS setting
        host = db_conf["host"]
        # Specifies the write capacity
        write_capacity_units = 10
        # Specifies the read capacity
        read_capacity_units = 10

    txn_id = UnicodeAttribute(hash_key=True)
    amount = NumberAttribute()
