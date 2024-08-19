from utils.env_handler import get_dynamodb_conf
from django.core.management.base import BaseCommand, CommandError
from pynamodb.models import Model


class Command(BaseCommand):
    help = 'Setup DynamoDB database'

    def add_arguments(self, parser):
        db_conf = get_dynamodb_conf()
        # host is optional argument
        parser.add_argument(
            "--host",
            help="""Set the DynamoDB host. By default, It will use aws cli default profile.
            For local development, use http://localhost:9999 or use DynamoDB host url.""",
            default=db_conf.get("host", "http://localhost:8000")
        )

        parser.add_argument(
            "--region",
            help="Set the DynamoDB region. Default value = us-west-2",
            default=db_conf["region"],
        )

    def handle(self, *args, **options):
        self.stdout.write('Running DynamoDB database setup...')
        try:
            # Get the host and region from the command line arguments
            host = options.get("host")
            print(f"DynamoDB host is set to {host}")
            region = options.get("region")
            print(f"DynamoDB region is set to {region}")
            print("Creating tables...")
            print(Model.__subclasses__())
            for model in Model.__subclasses__():
                # Set the host and region
                model.Meta.host = host
                model.Meta.region = region
                # Create the table
                model.create_table(
                    read_capacity_units=1,
                    write_capacity_units=1
                )
                print(f"{model.Meta.table_name} table is created successfully")
            print("DynamoDB database setup completed successfully!!")
        except Exception as e:
            CommandError(f"DynamoDB setup failed: {e}")
            print(f"[ERROR] DynamoDB setup failed: {e}")
