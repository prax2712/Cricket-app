from django.urls import path
from . import views

urlpatterns = [
    path('',views.homepageNonUser,name='homepageNonUser'),
    path('statistics/',views.statistics,name='statistics'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registration/', views.signup, name='signup'),
    path('<str:username>/',views.homepage,name='home'),
    path('liveHost/<str:matchId>/',views.live_host,name='liveHost'),
    path('liveView/<str:match_id>/',views.liveView,name='liveView'),
    path('player_selection/<str:match_id>/',views.player_selection,name='player_selection'),
    path('toss/<str:match_id>/', views.toss, name='toss'),
    path('hosting/<str:username>/', views.hosting, name='hosting'),
    path('match_summary/<int:match_id>/',views.match_summary,name='match_summary'),
]
