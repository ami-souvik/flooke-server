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

    def to_dict(self):
        result = dict()
        result["id"] = self.id
        result["owner"] = self.owner.to_dict()
        result["title"] = self.title
        result["body"] = self.body
        result["created_at"] = self.created_at
        result["updated_at"] = self.updated_at
        return result
