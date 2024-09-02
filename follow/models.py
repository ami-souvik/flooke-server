from django.conf import settings
from django.utils import timezone
from django.db.models import Model, ForeignKey, DateTimeField, CASCADE

# Create your models here.
class Follow(Model):
    """Follow model contains the relation details between user and community"""
    owner = ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        related_name="following",
        on_delete=CASCADE,
    )
    community = ForeignKey(
        'community.Community',
        null=False,
        related_name="followers",
        on_delete=CASCADE,
    )

    created_at = DateTimeField()
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
