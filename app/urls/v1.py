from django.urls import include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    ('auth/users/', include('basic_auth.urls')),
    ('token/', TokenObtainPairView.as_view(), { "name": 'token_obtain_pair' }),
    ('token/refresh/', TokenRefreshView.as_view(), { "name": 'token_refresh' }),
    ('content/', include('content.urls'))
]
