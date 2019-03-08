from django.contrib import admin
from django.urls import path, include
from .import views

app_name="basic"

urlpatterns = [
    path('index', views.index ,name='index'),
    path('chat/<str:room_name>', views.room ,name='room'),
]
