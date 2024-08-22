from django.conf import settings
from django.db.models import Model, ForeignKey, CharField, DateTimeField, CASCADE
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
        related_name="commentor",
        on_delete=CASCADE,
    )
    content = ForeignKey(
        'content.Content',
        null=False,
        related_name="article",
        on_delete=CASCADE,
    )
    body = CharField(max_length=1024, null=False)

    created_at = DateTimeField()
    updated_at = DateTimeField()

    objects = CommentQuerySet.as_manager()

