import os
import random
from itertools import batched
from django.utils import timezone
from django.core.management.base import BaseCommand, CommandError
from user.models import User
from content.models import Content
from comment.models import Comment
from django.contrib.auth.hashers import make_password

class Import:
    def __init__(self, start=1, num=10):
        self.start = start
        self.num = num
        path = 'utils/management/commands/mock'
        os.chdir(path)
        self.firstnames = []
        with open(f"firstnames.txt") as f:
            for line in f:
                [fname, gender] = line.split(";")
                self.firstnames.append((fname, gender.strip()))
        self.lastnames = []
        with open(f"lastnames.txt") as f:
            for line in f:
                self.lastnames.append(line.strip())
        self.contents = []
        self.content_comments = []
        with open(f"feed.txt") as f:
            is_content = True
            for line in f:
                if is_content:
                    [title, body] = line.split(";")
                    self.contents.append((title, body.strip()))
                else:
                    comms = line.split(";")
                    last = comms.pop().strip()
                    comms.append(last)
                    if not comms[0]:
                        self.content_comments.append([])
                    else:
                        self.content_comments.append(comms)
                is_content = not is_content
        self.contents_count = len(self.contents)

    def generate_user_info(self):
        firstname, gender = random.choice(self.firstnames)
        lastname = random.choice(self.lastnames)
        username = f"{firstname}{lastname}{round(random.random()*10000)}"
        email = f"{username}@gmail.com"
        return firstname, lastname, gender, username, email

    def generate_users(self):
        users = []
        print("Users:")
        for idx in range(self.num):
            random.seed(idx)
            firstname, lastname, gender, username, email = self.generate_user_info()
            print(firstname, lastname, gender, username, email)
            users.append(User(
                id=self.start+idx,
                username=username,
                password=make_password(username),
                first_name=firstname,
                last_name=lastname,
                email=email,
                gender=gender,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            ))
        return users

    def generate_contents(self, start=1):
        contents = []
        user = self.start
        count = 0
        for content in self.contents:
            title, body = content
            contents.append(Content(
                id=start+count,
                owner=User.objects.get(id=user),
                title=title,
                body=body,
                created_at=timezone.now(),
                updated_at=timezone.now(),
            ))
            count += 1
            user += 1
            if user > self.num:
                user = self.start
        return contents

    def generate_comments(self, start=1):
        comment_records = []
        user = self.start
        count = 0
        content_count = 0
        for comments in self.content_comments:
            for c in comments:
                comment_records.append(Comment(
                    id=start+count,
                    owner=User.objects.get(id=user),
                    content=Content.objects.get(id=start+content_count),
                    body=c,
                    created_at=timezone.now(),
                    updated_at=timezone.now(),
                ))
                count += 1
            content_count += 1
            user += 1
            if user > self.num:
                user = self.start
        return comment_records

class Command(BaseCommand):
    help = 'Initialize platform with some initial records'

    def add_arguments(self, parser):
        # parser.add_argument("schemas", nargs="+", type=str)
        parser.add_argument(
            "--all",
            action="store_true",
            help="Initialize all schemas",
        )
        pass

    def handle(self, *args, **options):
        self.stdout.write('Please make sure you have applied all the migrations before running this command')
        self.stdout.write('Initializing...')
        try:
            batch_size = 10
            generator = Import(start=1)
            users = generator.generate_users()
            for batch in batched(users, batch_size):
                User.objects.bulk_create(list(batch), batch_size)
            self.stdout.write('Successfully initialized Users')
            contents = generator.generate_contents()
            for batch in batched(contents, batch_size):
                Content.objects.bulk_create(list(batch), batch_size)
            self.stdout.write('Successfully initialized Contents')
            comments = generator.generate_comments()
            for batch in batched(comments, batch_size):
                Comment.objects.bulk_create(list(batch), batch_size)
            self.stdout.write('Successfully initialized Comments')
        except OSError as e:
            print(f"Error occurred while reading the records: {e}")
            CommandError(f"Error occurred while reading the records: {e}")
        except Exception as e:
            print(f"IntraSocial initialization failed: {e}")
            CommandError(f"IntraSocial initialization failed: {e}")
