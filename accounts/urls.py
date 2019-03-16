from django.contrib import admin
from django.urls import path, include
from .import views

app_name="accounts"

urlpatterns = [
    path('login', views.login ,name='login'),
    path('logout', views.logout ,name='logout'),
    path('register', views.register ,name='register'),
	path('check_username', views.isUsernameAvailable ,name='check_username'),
 
 	path('profile', views.profile ,name='profile'),
   	path('auth_setting', views.authSetting ,name='auth_setting'),
   	path('change_username', views.changeUsername ,name='change_username'),
    path('change_password', views.changePassword ,name='change_password'),
    path('delete_account', views.deleteAccount ,name='delete_account'),

    path('connected_users_search', views.connectedUsersSearch ,name='connected_users_search'),
    path('other_users_search', views.otherUsersSearch ,name='other_users_search'),
    # path('chat/<str:room_name>', views.room ,name='room'),
]
