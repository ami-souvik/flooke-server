from django.contrib.auth.backends import UserModel, BaseBackend, ModelBackend as DefaultModelBackend
from django.conf import settings
from django.contrib.auth.hashers import check_password
# from django.contrib.auth import get_user_model

# UserModel = get_user_model()

class ModelBackend(DefaultModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        return super().authenticate(request, username, password, **kwargs)
