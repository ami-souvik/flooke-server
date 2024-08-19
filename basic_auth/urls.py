from .views import AuthView
from django.urls import path

urlpatterns = [
    path('', AuthView.as_view()),
]
