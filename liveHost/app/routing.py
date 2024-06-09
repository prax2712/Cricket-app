from django.urls import path,re_path
from . import consumers

websocket_urlpatterns = [
    path('liveHost/<str:match_id>/',consumers.LiveHostWebsocket.as_asgi()),
    re_path(r"ws/match/(?P<match_id>\w+)/$", consumers.MatchView.as_asgi()),
]