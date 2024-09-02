from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, DateTimeField


class User(AbstractUser):
    """User model"""
    emoji_unicode = CharField(null=True)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
