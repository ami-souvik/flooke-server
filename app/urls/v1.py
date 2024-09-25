from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    ('token/', TokenObtainPairView.as_view(), { "name": 'token_obtain_pair' }),
    ('token/refresh/', TokenRefreshView.as_view(), { "name": 'token_refresh' }),
    ('token/verify/', TokenVerifyView.as_view(), { "name": 'token_verify' })
]