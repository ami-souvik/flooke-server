from django.db.models import Model, TextField, DateTimeField, ForeignKey, CASCADE
# from utils.models import Model
from users.models import Persona

# Create your models here.
class Post(Model):

    id = TextField(primary_key=True)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    user_id = ForeignKey(Persona, on_delete=CASCADE)
    content = TextField()

class Comment(Model):

    id = TextField(primary_key=True)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    # on_delete ref (https://docs.djangoproject.com/en/5.1/ref/models/fields/#django.db.models.ForeignKey.on_delete)
    post_id = ForeignKey(Post, on_delete=CASCADE)
    user_id = TextField()
    content = TextField()

class Like(Model):

    id = TextField(primary_key=True)
    created_at = DateTimeField()
    updated_at = DateTimeField()
    
    post_id = ForeignKey(Post, on_delete=CASCADE)
    user_id = TextField()
