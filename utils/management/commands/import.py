import json
import traceback
from itertools import batched
from django.utils import timezone
from django.db import transaction
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
        try:
            batch_size = 10
            # write to the file
            path = 'contents.json'
            print(f"Importing from {path}")
            data = dict()
            with open(path, 'r') as file:
                data = json.load(file)
            with transaction.atomic():
                users = []
                for u in data["users"]:
                    users.append(User(
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                        password=make_password(u["username"]),
                        **u
                    ))
                for batch in batched(users, batch_size):
                    User.objects.bulk_create(list(batch), batch_size)

                contents = []
                for c in data["contents"]:
                    if not isinstance(c["owner"], User):
                        c["owner"] = User.objects.get(id=c["owner"])
                    contents.append(Content(
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                        **c
                    ))
                for batch in batched(contents, batch_size):
                    Content.objects.bulk_create(list(batch), batch_size)

                content_comments = []
                for c in data["comments"]:
                    if not isinstance(c["owner"], User):
                        c["owner"] = User.objects.get(id=c["owner"])
                    if "content" in c:
                        c["content"] = Content.objects.get(id=c["content"])
                        content_comments.append(Comment(
                            created_at=timezone.now(),
                            updated_at=timezone.now(),
                            **c
                        ))
                for batch in batched(content_comments, batch_size):
                    Comment.objects.bulk_create(list(batch), batch_size)
                # comment_comments = []
                # for c in data["comments"]:
                #     if not isinstance(c["owner"], User):
                #         c["owner"] = User.objects.get(id=c["owner"])
                #     if "comment" in c:
                #         c["comment"] = Comment.objects.get(id=c["comment"])
                #         comment_comments.append(Comment(
                #             created_at=timezone.now(),
                #             updated_at=timezone.now(),
                #             **c
                #         ))
                # for batch in batched(comment_comments, batch_size):
                #     Comment.objects.bulk_create(list(batch), batch_size)

                feedbacks = []
                for f in data["feedbacks"]:
                    if not isinstance(f["user"], User):
                        f["user"] = User.objects.get(id=f["user"])
                    if "content" in f:
                        f["content"] = Content.objects.get(id=f["content"])
                    if "comment" in f:
                        f["comment"] = Comment.objects.get(id=f["comment"])
                    feedbacks.append(Feedback(
                        created_at=timezone.now(),
                        updated_at=timezone.now(),
                        **f
                    ))
                for batch in batched(feedbacks, batch_size):
                    Feedback.objects.bulk_create(list(batch), batch_size)

            self.stdout.write('Done!! Successfully Imported')
        except OSError as e:
            print(f"Error occurred while reading the records: {e}")
            raise CommandError(f"Error occurred while reading the records: {e}")
        except Exception as e:
            print(f"IntraSocial initialization failed:\n{traceback.format_exc()}")
            raise CommandError(f"IntraSocial initialization failed: {e}")
