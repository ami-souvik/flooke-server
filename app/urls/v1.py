from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    ('token/', TokenObtainPairView.as_view(), { "name": 'token_obtain_pair' }),
    ('token/refresh/', TokenRefreshView.as_view(), { "name": 'token_refresh' })
]