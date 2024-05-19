from django.urls import re_path, path
from . import consumers

websocket_urlpatterns = [
    path(r'ws/jeopardy/<str:room_id>/', consumers.JeopardyConsumer.as_asgi())
]