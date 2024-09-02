import os
from itertools import batched
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from user.models import User
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Initialize IntraSocial platform with some initial records'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write('Please make sure you have applied all the migrations before running this command')
        self.stdout.write('Initializing IntraSocial...')
        try:
            batch_size = 10
            path = 'utils/management/commands/records'
            os.chdir(path)
            start_id = 31
            users = []
            with open(f"init_user.txt") as f:
                for line in f:
                    parts = line.split(";")
                    users.append(User(
                        id=start_id,
                        username=parts[0],
                        password=make_password(parts[1]),
                        first_name=parts[2],
                        last_name=parts[3],
                        email=parts[4],
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                    ))
                    start_id += 1
            for batch in batched(users, batch_size):
                User.objects.bulk_create(list(batch), batch_size)
            self.stdout.write('Successfully initialized IntraSocial')
        except OSError as e:
            print(f"Error occurred while reading the records: {e}")
            CommandError(f"Error occurred while reading the records: {e}")
        except Exception as e:
            print(f"IntraSocial initialization failed: {e}")
            CommandError(f"IntraSocial initialization failed: {e}")
