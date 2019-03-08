from django.contrib import admin
from django.urls import path, include
from .import views

app_name="connections"

urlpatterns = [
    path('add_connection', views.addConnection ,name='add_connection'),
    path('delete_connection', views.deleteConnection ,name='delete_connection'),
    path('confirm_connection', views.confirmConnection ,name='confirm_connection'),
    # path('chat/<str:room_name>', views.room ,name='room'),
]
