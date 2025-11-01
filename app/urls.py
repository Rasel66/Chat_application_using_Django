from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home_view, name="home"),
    path('chat/', chat_view, name='chat'),
    path('signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout_user'),
    path('profile/', profile_view, name='profile'),
    path('activate/<domain>/<uidb64>/<token>/', activate, name='activate'),

    path('accounts/', include('django.contrib.auth.urls')),
]
