from .views import ContentView
from django.urls import path

urlpatterns = [
    path('', ContentView.as_view()),
]
