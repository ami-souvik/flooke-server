from utils.env_handler import get_dynamodb_conf
from django.core.management.base import BaseCommand, CommandError
from pynamodb.models import Model
from transaction.models import Transaction
import boto3

# Create a DynamoDB client
db_conf = get_dynamodb_conf()
dynamodb = boto3.client('dynamodb', 
                        endpoint_url=db_conf["host"], 
                        region_name=db_conf["region"]) 


class Command(BaseCommand):
    help = 'Setup DynamoDB database'

    def add_arguments(self, parser):
        # host is optional argument
        parser.add_argument(
            "--host",
            help="""Set the DynamoDB host. By default, It will use aws cli default profile.
            For local development, use http://localhost:9999 or use DynamoDB host url.""",
            default=db_conf["host"]
        )

        parser.add_argument(
            "--region",
            help="Set the DynamoDB region. Default value = us-west-2",
            default=db_conf["region"],
        )

    def handle(self, *args, **options):
        self.stdout.write('Running DynamoDB database setup...')
        try:
            # Create a table
            table_name = 'my_table'
            dynamodb.create_table(
                TableName=table_name,
                KeySchema=[
                    {'AttributeName': 'id', 'KeyType': 'HASH'}
                ],
                AttributeDefinitions=[
                    {'AttributeName': 'id', 'AttributeType': 'S'}
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            )
            print("DynamoDB database setup completed successfully!!")
        except Exception as e:
            print(f"[ERORR] DynamoDB setup failed: {e}")
            CommandError(f"[ERORR] DynamoDB setup failed: {e}")
