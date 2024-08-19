from django.db.models import Model, TextField, EmailField, DateTimeField
# from utils.models import Model

# Create your models here.
class Persona(Model):

    id = TextField(primary_key=True)
    created_at = DateTimeField()
    updated_at = DateTimeField()

    username = TextField()
    email = EmailField()
    name = TextField()
    bio = TextField()
