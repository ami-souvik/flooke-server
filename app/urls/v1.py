from django.urls import include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    ('token/', TokenObtainPairView.as_view(), { "name": 'token_obtain_pair' }),
    ('token/refresh/', TokenRefreshView.as_view(), { "name": 'token_refresh' }),
    ('users/', include('basic_auth.urls')),
    ('content/', include('content.urls'))
]
