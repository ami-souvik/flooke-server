from django.db.models import Model as djangoModel, TextField, DateTimeField

class Model(djangoModel):
    
    id = TextField(primary_key=True)
    created_at = DateTimeField()
    updated_at = DateTimeField()
