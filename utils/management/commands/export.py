import os
import random
import json
from itertools import batched
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from user.models import User
from content.models import Content
from comment.models import Comment
from feedback.models import Feedback
from django.contrib.auth.hashers import make_password

class Export:
    def __init__(self):
        pass

class Command(BaseCommand):
    help = 'Initialize platform with some initial records'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        self.stdout.write('Exporting...')
        try:
            # write to the file
            path = 'utils/management/commands/mock/export.json'
            print(f"Output file is set to {path}")
            users = User.objects.all()
            _users = []
            contents = Content.objects.all()
            _contents = []
            comments = Comment.objects.all()
            _comments = []
            feedbacks = Feedback.objects.all()
            _feedbacks = []
            with open(path, 'w') as file:
                for u in users:
                    _users.append(u.to_dict())
                for c in contents:
                    _contents.append(c.to_dict())
                for c in comments:
                    _comments.append(c.to_dict())
                for f in feedbacks:
                    _feedbacks.append(f.to_dict())
                file.write(json.dumps({
                    "users": _users,
                    "contents": _contents,
                    "comments": _comments,
                    "feedbacks": _feedbacks
                }, indent=2))
            self.stdout.write('Done!! Successfully Exported')
        except OSError as e:
            print(f"Error occurred while reading the records: {e}")
            CommandError(f"Error occurred while reading the records: {e}")
        except Exception as e:
            print(f"IntraSocial initialization failed: {e}")
            CommandError(f"IntraSocial initialization failed: {e}")
