from .views import CommentView
from django.urls import path

urlpatterns = [
    path('<str:content_id>', CommentView.as_view()),
]
