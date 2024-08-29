from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models import Model, ForeignKey, DateTimeField, CASCADE

class Like(Model):
    """Like model contains user liked contents or comments"""
    user = ForeignKey(
        settings.AUTH_USER_MODEL,
        null=False,
        related_name="likes",
        on_delete=CASCADE,
    )
    content = ForeignKey(
        'content.Content',
        null=True,
        related_name="likes",
        on_delete=CASCADE,
    )
    comment = ForeignKey(
        'comment.Comment',
        null=True,
        related_name="likes",
        on_delete=CASCADE,
    )

    created_at = DateTimeField()
    updated_at = DateTimeField()

    def clean(self):
        raise ValidationError("Like already exist")

    def validate_unique(self, exclude=None):
        if Like.objects.filter(user=self.user, content=self.content, comment=self.comment)\
            .exists():
            raise ValidationError("Like already exist")
        super(Like, self).validate_unique(exclude=exclude)

    def save(self, *args, **kwargs):
        self.validate_unique()
        if not self.created_at:
            self.created_at = timezone.now()
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)

    def to_dict(self):
        result = dict()
        result["id"] = self.id
        result["user"] = self.user.to_dict()
        result["content"] = self.content.to_dict()
        result["comment"] = self.comment.to_dict()
        result["created_at"] = self.created_at
        result["updated_at"] = self.updated_at
        return result
