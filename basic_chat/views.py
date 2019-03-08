from django.shortcuts import render
from django.http import HttpResponse
from django.utils.safestring import mark_safe
import json

def index(request):
	return render(request,'basic_chat/index.html')

def room(request, room_name):
    return render(request, 'basic_chat/chatroom/chatroom_layout.html', {
        'room_name_json': mark_safe(json.dumps(room_name)),
        'room_name':room_name,
        'page_title':room_name,
    })