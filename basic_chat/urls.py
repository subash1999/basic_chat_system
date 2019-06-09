from django.contrib import admin
from django.urls import path, include
from .import views

app_name="chat"

urlpatterns = [
    path('index', views.index ,name='index'),
    path('t/<str:thread_id>', views.chat ,name='chat'),
    path('new_msg', views.newMsg ,name='new_msg'),
    path('update_status', views.updateStatus ,name='update_status'),
]
