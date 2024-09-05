from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.db.models import CharField, DateTimeField

gender_choices = (
    ("M", "Male"),
    ("F", "Female")
)

class User(AbstractUser):
    """User model"""
    emoji_unicode = CharField(null=True)
    gender = CharField(
        null=True,
        max_length=1,
        choices=gender_choices
    )
    created_at = DateTimeField()
    updated_at = DateTimeField()

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def to_dict(self):
        return dict(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            username=self.username,
            email=self.email,
            emoji_unicode=self.emoji_unicode,
            gender=self.gender
        )
