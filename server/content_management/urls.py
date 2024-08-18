from .views import CreatePost
from django.urls import path

urlpatterns = [
    path('', CreatePost.as_view()),
]
