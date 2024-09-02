from django.utils import timezone
from django.db.models import Model, TextField, CharField, DateTimeField

# Create your models here.
class Community(Model):
    """Community model contains the community details"""
    title = CharField(max_length=255, null=False)
    body = TextField(null=False)

    created_at = DateTimeField()
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)