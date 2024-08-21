from django.conf import settings
from django.db.models import Model, ForeignKey, CharField, DateTimeField, CASCADE
from django.db.models.query import QuerySet

class ContentQuerySet(QuerySet):
    """Personalized queryset created to improve model usability"""
    pass

class Content(Model):
    """Content model contains user posted content"""
    owner = ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        related_name="creator",
        on_delete=CASCADE,
    )
    title = CharField(max_length=255, null=False)
    body = CharField(max_length=1024, null=False)

    created_at = DateTimeField()
    updated_at = DateTimeField()

    objects = ContentQuerySet.as_manager()

