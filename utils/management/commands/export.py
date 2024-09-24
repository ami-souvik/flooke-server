import json
from django.core.management.base import BaseCommand, CommandError
from user.models import User
from content.models import Content
from comment.models import Comment
from feedback.models import Feedback

class Export:
    def __init__(self):
        pass

class Command(BaseCommand):
    help = 'Exports contents'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write('Exporting...')
        try:
            # write to the file
            path = 'contents.json'
            print(f"Output file is set to {path}")
            users = User.objects.all()
            _users = []
            contents = Content.objects.all()
            _contents = []
            with open(path, 'w') as file:
                for u in users:
                    _users.append(u.to_dict())
                # TODO: Contents export is not properly implemented
                for c in contents:
                    _contents.append(c.to_dict())
                file.write(json.dumps({
                    "users": _users,
                    "contents": _contents
                }, indent=2))
            self.stdout.write('Done!! Successfully Exported')
        except OSError as e:
            print(f"Error occurred while reading the records: {e}")
            CommandError(f"Error occurred while reading the records: {e}")
        except Exception as e:
            print(f"IntraSocial initialization failed: {e}")
            CommandError(f"IntraSocial initialization failed: {e}")
