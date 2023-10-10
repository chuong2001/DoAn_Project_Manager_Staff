from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/chat/$', consumers.ChatConsumer.as_asgi()),
]
from django.urls import path, include

urlpatterns = [
    path('', include('chat.routing.websocket_urlpatterns')),
    # ...
]
