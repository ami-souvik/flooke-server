from django.conf.urls import include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    ('token/', TokenObtainPairView.as_view(), { "name": 'token_obtain_pair' }),
    ('token/refresh/', TokenRefreshView.as_view(), { "name": 'token_refresh' }),
    ('chat/', include("conversation.urls"))
]