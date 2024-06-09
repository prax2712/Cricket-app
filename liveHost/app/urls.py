from django.urls import path
from . import views

urlpatterns = [
    path('liveHost/<str:matchId>/',views.live_host),
    path('liveView/<str:match_id>/',views.liveView,name='liveView'),
    path('statistics/',views.statistics,name='statistics'),
    path('player_selection/<str:match_id>/',views.player_selection,name='player_selection'),
    path('<str:username>/',views.homepage,name='homepage'),
    path('',views.homepageNonUser,name='homepageNonUser'),
    path('toss/<str:match_id>/', views.toss, name='toss'),
    path('login/', views.login, name='login'),
    path('registration/', views.signup, name='signup'),
    path('hosting/<str:username>/', views.hosting, name='hosting'),
]