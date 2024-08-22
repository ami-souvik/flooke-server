from .views import AuthView, UpdateUserView
from django.urls import path

urlpatterns = [
    path('', AuthView.as_view()),
    path('update/', UpdateUserView.as_view()),
]
