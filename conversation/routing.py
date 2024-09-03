from django.urls import re_path

from .consumers import ConversationConsumer

websocket_urlpatterns = [
    re_path(r"ws/chat/(?P<room_name>\w+)/$", ConversationConsumer.as_asgi()),
]