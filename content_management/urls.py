from .views.post_view import PostOps, GetPostsByUser
from .views.like_view import LikeOps
from django.urls import path

urlpatterns = [
    path('', PostOps.as_view()),
    path('like/<str:post_id>', LikeOps.as_view()),
    path('post/<str:user_id>', GetPostsByUser.as_view()),
]
