from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Model, ForeignKey, BooleanField, CharField, DateTimeField, CASCADE
from django.db.models.query import QuerySet

class CommentQuerySet(QuerySet):
    """Personalized queryset created to improve model usability"""
    def all_by_content(self, content_id):
        return self.filter(content=content_id)

class Comment(Model):
    """Content model contains user posted content"""
    owner = ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        related_name="comments",
        on_delete=CASCADE,
    )
    content = ForeignKey(
        'content.Content',
        null=True,
        related_name="comments",
        on_delete=CASCADE,
    )
    comment = ForeignKey(
        'comment.Comment',
        null=True,
        related_name="comments",
        on_delete=CASCADE,
    )
    body = CharField(max_length=1024, null=False)
    has_reply = BooleanField(null=False, default=False)

    created_at = DateTimeField()
    updated_at = DateTimeField()

    objects = CommentQuerySet.as_manager()

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)
