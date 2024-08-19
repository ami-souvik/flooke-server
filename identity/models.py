from django.contrib.auth.models import AbstractUser
from django.db.models import DateTimeField


class Identity(AbstractUser):
    """User model"""
    created_at = DateTimeField()
    updated_at = DateTimeField()
