from django.conf import settings
from django.db.models import Model, ForeignKey, CharField, DateTimeField, CASCADE
from django.db.models.query import QuerySet
from markdownfield.models import MarkdownField, RenderedMarkdownField
from markdownfield.validators import VALIDATOR_STANDARD

class ContentQuerySet(QuerySet):
    """Personalized queryset created to improve model usability"""
    def get_all(self):
        """[STARTING]: Initially we are returning all the contents"""
        return self.all()

class Content(Model):
    """Content model contains user posted content"""
    owner = ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        related_name="creator",
        on_delete=CASCADE,
    )
    title = CharField(max_length=255, null=False)
    body = MarkdownField(rendered_field='text_rendered', validator=VALIDATOR_STANDARD)
    text_rendered = RenderedMarkdownField()

    created_at = DateTimeField()
    updated_at = DateTimeField()

    objects = ContentQuerySet.as_manager()
