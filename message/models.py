from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Model, ForeignKey, DateTimeField, TextField, CASCADE

# Create your models here.
class Message(Model):
    """Message model contains the message context"""
    sender = ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        related_name="messages",
        on_delete=CASCADE,
    )
    conversation = ForeignKey(
        'conversation.Conversation',
        null=False,
        related_name="messages",
        on_delete=CASCADE,
    )
    content = TextField()

    created_at = DateTimeField()
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        self.validate_unique()
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
