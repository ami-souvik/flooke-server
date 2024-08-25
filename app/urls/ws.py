from django.urls import path
from chat.consumers import ChatConsumer

urlpatterns = [
    path('chat/', ChatConsumer.as_asgi())
]