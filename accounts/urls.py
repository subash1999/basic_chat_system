from django.contrib import admin
from django.urls import path, include
from .import views

app_name="accounts"

urlpatterns = [
    path('login', views.login ,name='login'),
    path('logout', views.logout ,name='logout'),
    path('register', views.register ,name='register'),
    path('check_username', views.isUsernameAvailable ,name='check_username'),

    # path('chat/<str:room_name>', views.room ,name='room'),
]
