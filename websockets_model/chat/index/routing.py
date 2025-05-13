from django.urls import re_path

from . import consumers
websocket_urlpatterns=[

 re_path("new_friend",consumers.handle_add_friend.as_asgi())

]