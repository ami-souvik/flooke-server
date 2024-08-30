from django.db.models import Model, DateTimeField

# Create your models here.
class Chat(Model):
    """Chat model contains the conversational messages among users"""
    created_at = DateTimeField()
    updated_at = DateTimeField()